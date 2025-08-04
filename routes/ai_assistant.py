import google.generativeai as genai
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime

from database import database_config, schemas, models
from config import settings
from routes.user_dashboard import get_current_active_user, get_user_meals_by_date


genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)


def get_db():
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ask")
def ask_ai_assistant(
    chat_request: schemas.AIChatRequest,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    
    user_info = (
        f"User Profile: Age {current_user.age}, Gender {current_user.gender}, "
        f"Weight {current_user.weight}kg, Height {current_user.height}cm. "
        f"The user's primary goal is '{current_user.goal}'."
    )

    todays_meals = get_user_meals_by_date(db, user_id=current_user.id, log_date=datetime.utcnow().date())
    
    if todays_meals:
        meals_str = ". ".join([f"{meal.meal_type} consisted of {meal.food_items}" for meal in todays_meals])
        food_info = f"So far today, the user has eaten: {meals_str}."
    else:
        food_info = "The user has not logged any meals yet today."

   
    system_prompt = (
        "You are a helpful and friendly AI nutrition assistant. Your name is Spano. "
        "You provide supportive and brief advice based on the user's profile, goals, and food intake. "
        "Do not give medical advice. Keep your answers concise and easy to understand, like a chat message. "
        "Here is the user's information: "
        f"{user_info} {food_info}"
    )

    full_prompt = f"{system_prompt}\n\nUser's question: '{chat_request.prompt}'"

    try:
        response = model.generate_content(full_prompt)
        return {"response": response.text}
    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI assistant is currently unavailable. Please try again later."
        )
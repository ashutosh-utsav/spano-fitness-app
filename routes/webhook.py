import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import database_config, schemas, models

from routes.auth import get_user_by_name
from routes.user_dashboard import create_user_meal

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"]
)

def get_db():
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.WebhookResponse)
def handle_webhook(
    payload: schemas.WebhookMessage,
    db: Session = Depends(get_db)
):
    """
    Handles an incoming webhook to log a meal from a message.
    
    Expected message format: "log <meal_type>: <item1>, <item2>, ..."
    Example: "log lunch: Jeera Rice, Dal"
    """

    user = get_user_by_name(db, name=payload.user_name)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{payload.user_name}' not found."
        )

    message = payload.message.strip().lower()
   
    match = re.match(r"^log\s+([a-zA-Z]+):\s*(.+)$", message)
    
    if not match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid message format. Expected 'log <meal_type>: <items>'."
        )
        
    meal_type = match.group(1).capitalize()
    food_items_str = match.group(2)

    meal_data = schemas.MealLogCreate(
        meal_type=meal_type,
        food_items=food_items_str
    )
    
    create_user_meal(db=db, meal=meal_data, user_id=user.id)

    return {
        "status": "success",
        "detail": f"Successfully logged {meal_type} for user {payload.user_name}."
    }
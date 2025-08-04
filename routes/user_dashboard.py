from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import date, datetime, time

from database import database_config, schemas, models
from config import settings

router = APIRouter(
    tags=["User Dashboard Pages"]
)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def get_current_active_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_302_FOUND,
        headers={"Location": "/login"},
    )
    if not token:
        raise credentials_exception
    
    try:
        token = token.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (JWTError, IndexError):
        raise credentials_exception
    
    user = get_user_by_name(db, name=username)
    if user is None:
        raise credentials_exception
    return user

def calculate_bmr(gender: str, weight: float, height: float, age: int) -> float:
    if gender.lower() == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == "female":
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return 0.0

food_db = {
    "jeera rice": {"calories": 250, "protein": 5, "carbs": 45, "fiber": 2},
    "dal": {"calories": 180, "protein": 12, "carbs": 20, "fiber": 5},
    "cucumber": {"calories": 16, "protein": 1, "carbs": 4, "fiber": 1},
}

def create_user_meal(db: Session, meal: schemas.MealLogCreate, user_id: int):
    db_meal = models.MealLog(**meal.dict(), user_id=user_id)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def get_user_meals_by_date(db: Session, user_id: int, log_date: date):
    start_of_day = datetime.combine(log_date, time.min)
    end_of_day = datetime.combine(log_date, time.max)
    return db.query(models.MealLog).filter(
        models.MealLog.user_id == user_id,
        models.MealLog.logged_at >= start_of_day,
        models.MealLog.logged_at <= end_of_day
    ).all()


@router.get("/dashboard", response_class=HTMLResponse)
def user_dashboard(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    bmr = calculate_bmr(current_user.gender, current_user.weight, current_user.height, current_user.age)


    todays_meals = get_user_meals_by_date(db=db, user_id=current_user.id, log_date=datetime.utcnow().date())
    
    total_nutrients = {"calories": 0, "protein": 0, "carbs": 0, "fiber": 0}
    for meal in todays_meals:
        items = [item.strip().lower() for item in meal.food_items.split(',')]
        for item_name in items:
            if item_name in food_db:
                for nutrient, value in food_db[item_name].items():
                    total_nutrients[nutrient] += value
    
    status_data = {
        "bmr": round(bmr, 2),
        "todays_intake": total_nutrients,
        "todays_meals": todays_meals
    }
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "status": status_data})

@router.post("/dashboard/log-meal")
def log_meal_form(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
    meal_type: str = Form(...),
    food_items: str = Form(...)
):
    meal_data = schemas.MealLogCreate(meal_type=meal_type, food_items=food_items)
    create_user_meal(db=db, meal=meal_data, user_id=current_user.id)
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
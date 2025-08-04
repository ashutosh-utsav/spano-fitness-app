from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class MealLogBase(BaseModel):
    meal_type: str
    food_items: str

class MealLogCreate(MealLogBase):
    pass

class MealLog(MealLogBase):
    id: int
    logged_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    gender: str
    goal: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    meals: List[MealLog] = []

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: Optional[str] = None

class WebhookMessage(BaseModel):
    user_name: str
    message: str

class WebhookResponse(BaseModel):
    status: str
    detail: str

class AIChatRequest(BaseModel):
    prompt: str

import datetime
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database_config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    gender = Column(String)
    goal = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    meals = relationship("MealLog", back_populates="owner")


class MealLog(Base):
    __tablename__ = "meallogs"

    id = Column(Integer, primary_key=True, index=True)
    meal_type = Column(String, index=True)
    food_items = Column(String)
    logged_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="meals")
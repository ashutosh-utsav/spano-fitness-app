from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from database import database_config, schemas, models
from routes.user_dashboard import get_current_active_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin Pages"]
)

templates = Jinja2Templates(directory="templates")


def get_db():
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_admin_user(current_user: models.User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

@router.get("/dashboard", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin_user)
):
    users = get_all_users(db)
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "users": users})
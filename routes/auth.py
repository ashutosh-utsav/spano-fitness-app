from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import database_config, schemas, models
from security import security_config

router = APIRouter(
    tags=["Authentication Pages"]
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

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security_config.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        hashed_password=hashed_password,
        age=user.age,
        weight=user.weight,
        height=user.height,
        gender=user.gender,
        goal=user.goal
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_form(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    user = get_user_by_name(db, name=username)
    if not user or not security_config.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

    access_token = security_config.create_access_token(data={"sub": user.name})
    
   
    redirect_url = "/admin/dashboard" if user.is_admin else "/dashboard"
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
def signup_form(
    request: Request,
    db: Session = Depends(get_db),
    name: str = Form(...),
    password: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    height: float = Form(...),
    gender: str = Form(...),
    goal: str = Form(...)
):
    db_user = get_user_by_name(db, name=name)
    if db_user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Username already registered"})
    
    user_data = schemas.UserCreate(
        name=name, password=password, age=age, weight=weight, height=height, gender=gender, goal=goal
    )
    create_user(db=db, user=user_data)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.get("/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")
    return response
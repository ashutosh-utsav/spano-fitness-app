from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# New imports for the startup event
from config import settings
from database.schemas import UserCreate
from routes.auth import get_user_by_name, create_user

from database import database_config, models
from routes import auth, user_dashboard, admin, webhook, ai_assistant
from routes.user_dashboard import get_current_active_user

# This command tells SQLAlchemy to create all the tables defined in models.py
models.Base.metadata.create_all(bind=database_config.engine)

app = FastAPI(
    title="Spano Fitness API",
    description="API for user authentication, BMR calculation, and meal logging with an AI assistant.",
    version="1.0.0",
)

# --- NEW: STARTUP EVENT TO CREATE DEFAULT USERS ---
@app.on_event("startup")
def create_initial_users():
    db = database_config.SessionLocal()
    try:
        # Check for and create default user
        default_user = get_user_by_name(db, name=settings.DEFAULT_USER_USERNAME)
        if not default_user:
            user_in = UserCreate(
                name=settings.DEFAULT_USER_USERNAME,
                password=settings.DEFAULT_USER_PASSWORD,
                age=30, weight=70, height=175, gender="male", goal="maintenance"
            )
            create_user(db, user=user_in)
            print("Default user created.")

        # Check for and create default admin
        default_admin = get_user_by_name(db, name=settings.DEFAULT_ADMIN_USERNAME)
        if not default_admin:
            admin_in = UserCreate(
                name=settings.DEFAULT_ADMIN_USERNAME,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                age=40, weight=80, height=180, gender="male", goal="admin tasks"
            )
            # Create the user first
            new_admin = create_user(db, user=admin_in)
            # Then update the 'is_admin' flag
            new_admin.is_admin = True
            db.commit()
            print("Default admin created.")

    finally:
        db.close()
# --- END OF NEW SECTION ---

# Configure Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Middleware to add user to request state
@app.middleware("http")
async def add_user_to_state(request: Request, call_next):
    db = database_config.SessionLocal()
    try:
        token = request.cookies.get("access_token")
        if token:
            parts = token.split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
            
            try:
                user = get_current_active_user(request=request, db=db)
                request.state.user = user
            except Exception:
                request.state.user = None
        else:
            request.state.user = None
    finally:
        db.close()
    
    response = await call_next(request)
    return response

# Include all the routers
app.include_router(auth.router)
app.include_router(user_dashboard.router)
app.include_router(admin.router)
app.include_router(webhook.router)
app.include_router(ai_assistant.router)

@app.get("/", tags=["Root"])
def read_root(request: Request):
    if request.state.user:
        if request.state.user.is_admin:
            return RedirectResponse(url="/admin/dashboard")
        return RedirectResponse(url="/dashboard")
    return RedirectResponse(url="/login")

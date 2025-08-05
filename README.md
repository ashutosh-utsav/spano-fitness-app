# Spano AI Fitness Tracker

### The Project is deployed and live at - https://spano.chagadiye.xyz/login
## Live-Link - [Live-link-for-app](https://spano.chagadiye.xyz/login)  

A **full-stack web application** built with **FastAPI** that serves as your **personal fitness and nutrition tracker**. Spano allows users to sign up, log their meals, and monitor their nutritional intake relative to their Basal Metabolic Rate (BMR). 

It also features a **secure authentication system**, distinct **user and admin roles**, and an **AI-powered nutrition assistant** to provide personalized advice.

---

## Features

### 1. Secure User Authentication
- Login, signup, and logout functionality.
- JWT tokens stored in **secure HttpOnly cookies**.

### 2. Persistent Database
- Built using **SQLite** and **SQLAlchemy ORM**.
- All user and meal data stored persistently.

### 3. Automatic User Creation
- Automatically creates a **default admin** and a **test user** on first startup for easy access and testing.

### 4. User Dashboard
Each user gets a personalized dashboard that displays:
- Calculated **Basal Metabolic Rate (BMR)**.
- Daily intake summary: **Calories**, **Protein**, **Carbs**, and **Fiber**.
- A quick form to log meals (Breakfast, Lunch, Dinner, Snack).
- A table listing all meals logged for the current day.

### 5. Admin Dashboard
- Secure, **admin-only** access.
- View a **list of all registered users** in the system.

### 6. AI Nutrition Assistant
- Integrated **chatbot powered by Google’s Gemini API**.
- Provides **personalized nutritional feedback** and **diet advice** based on user profile, goals, and meal logs.

### 7. Webhook Integration
- A `/webhook` endpoint available to **log meals programmatically** from external services or devices.



## Project Structure

```bash
/spano-fitness-app
|
|-- /database
|   |-- database_config.py
|   |-- models.py
|   |-- schemas.py
|
|-- /routes
|   |-- auth.py
|   |-- user_dashboard.py
|   |-- admin.py
|   |-- webhook.py
|   |-- ai_assistant.py
|
|-- /security
|   |-- security_config.py
|
|-- /templates
|   |-- base.html
|   |-- login.html
|   |-- signup.html
|   |-- dashboard.html
|   |-- admin_dashboard.html
|
|-- .env
|-- .gitignore
|-- config.py
|-- main.py
|-- README.md
|-- requirements.txt
```


### Setup and InstallationFollow these steps to get the application running locally.
#### 1. Clone the Repository
```bash
git clone git@github.com:ashutosh-utsav/spano-fitness-app.git
cd spano-fitness-app
```

#### 2. Create and Activate a Virtual EnvironmentIt
```bash
# Install UV(A better and fast Python pkg manager)

uv venv
source .venv/bin/activate  #for linux/mac 

.\.venv\Scripts\activate  #for windows
```
#### 3. Sync The Dependencies 
```bash
uv sync
```
#### 4. Set Up Environment VariablesYou need to create a .env file in the root directory of the project. You can copy the example below.Create a file named .env and add the following content:

```bash
# You can generate one with: openssl rand -hex 32
SECRET_KEY="a-very-long-and-super-secret-random-string-for-jwt"

# The algorithm for JWT signing
ALGORITHM="HS256"

# How long a login session lasts in minutes
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Your API key from Google AI Studio (https://aistudio.google.com/)
GEMINI_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"

# Credentials for the default user created on first startup
DEFAULT_USER_USERNAME="user"
DEFAULT_USER_PASSWORD="password"

# Credentials for the default admin created on first startup
DEFAULT_ADMIN_USERNAME="admin"
DEFAULT_ADMIN_PASSWORD="password"
```

#### 5. Run the ApplicationUse uvicorn to run the FastAPI server. 
```bash
uvicorn main:app --reload
```

#### The server will be running at http://127.0.0.1:8000.

## How to Use
- Navigate to the App: Open your web browser and go to http://127.0.0.1:8000.

- Login: The application creates two users for you on the first run. You can log in with:

- Admin: username admin, password password

- Regular User: username user, password password

- Sign Up: You can also create your own accounts through the "Sign Up" page.

- Use the Dashboard: As a regular user, you can log your meals and chat with the AI assistant.

- Admin View: When you log in as an admin, you will be taken to the admin dashboard where you can see all registered users.
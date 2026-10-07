#This boilerplate uses FastAPI's built-in security utilities (OAuth2PasswordBearer and OAuth2PasswordRequestForm) to handle user login, password verification, and token generation

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI(title="Authentication API")

# 1. FastAPI Security Rule: Tells FastAPI where the client gets the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Mock Database
users_db = {
    "jubayer": {"username": "jubayer", "password": "secretpassword123"}
}

# 2. Login Route: Accepts form data (username & password) and returns a token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": form_data.username, "token_type": "bearer"}

# 3. Protected Dependency: Decodes token & verifies user
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = users_db.get(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user

# 4. Protected Route: Only accessible if a valid Bearer token is provided
@app.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user["username"], "status": "Authenticated"}

from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from utility.auth_helper import create_access_token, encrypt_password, verify_password
from typing import Optional
from datetime import datetime, timedelta
from model import *
import bcrypt
from utility.auth_bearer import JWTBearer
from fastapi.responses import JSONResponse
import logging
from utility.auth_helper import fake_users_db



logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# Signup endpoint
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(signup_request: SignupRequest):
    if signup_request.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    if any(user["email"] == signup_request.email for user in fake_users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )

    # Hash the password and store user data
    hashed_password = hash_password(signup_request.password)
    fake_users_db[signup_request.username] = {
        "username": signup_request.username,
        "email": signup_request.email,
        "password": hashed_password,
        'role': signup_request.user
    }
    return {"message": "User signed up successfully"}


# Protected route (requires authentication)
@router.get("/protected",dependencies=[Depends(JWTBearer())])
async def protected_route(name,token: str =Depends(JWTBearer())):
    return {"message": f"{name} you have access to this protected route!", "user": token}




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

router = APIRouter(tags=['Authentication'])


logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Login endpoint
@router.post("/login")
async def login(login_request: LoginRequest):
        user = None
        if login_request.username:
            user = fake_users_db.get(login_request.username)
        # If user doesn't exist or password doesn't match
        if not user or not verify_password(login_request.password, user['password']):
            error_msg = "Incorrect email or password"
            logger.error(error_msg)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_msg)

        # Checking if the user is active
        # if user['status'] != 1:
        #     error_msg = "User is not active"
        #     logger.error(error_msg)
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not active")

        # Generating JWT Token
        jwtdata = {
            "email": login_request.username,
            "role": user['role']
        }
        jwt_token = create_access_token(jwtdata)

        # Preparing response data
        response_data = {
            "message": "User login successfully",
            "email": login_request.username,
            "jwt_token": jwt_token
        }
        return JSONResponse(content=response_data)
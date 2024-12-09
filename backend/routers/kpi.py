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

router = APIRouter(prefix="/kpi", tags=["Users"])




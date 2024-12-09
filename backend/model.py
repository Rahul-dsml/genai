
from pydantic import BaseModel
from typing import Optional


# Pydantic models
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str
    user: str

class LoginRequest(BaseModel):
    username: str
    password: str
    user:str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# Define a model for the input JSON
class SummarizerInput(BaseModel):
    query: str
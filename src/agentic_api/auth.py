# src/agentic_api/auth.py

import os
import time
from typing import Dict, Optional
from datetime import datetime, timedelta

import boto3
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# Load environment variables
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
COGNITO_USER_POOL_ID = os.getenv("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.getenv("COGNITO_APP_CLIENT_ID")
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CALLBACK_URL = os.getenv("COGNITO_CALLBACK_URL")
COGNITO_LOGOUT_URL = os.getenv("COGNITO_LOGOUT_URL")

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Initialize Cognito client
cognito_idp = boto3.client('cognito-idp', region_name=AWS_REGION)

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_at: int

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[int] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Authentication functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return encoded_jwt, int(expire.timestamp())

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate and return the current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, exp=exp)
    except JWTError:
        raise credentials_exception
    
    # Check if token is expired
    if token_data.exp and token_data.exp < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # In a real application, you would fetch the user from a database
    # Here we're just returning the username from the token
    user = User(username=token_data.username, disabled=False)
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Check if the current user is active"""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# AWS Cognito functions
def get_cognito_login_url():
    """Generate the Cognito hosted UI login URL"""
    return f"https://{COGNITO_DOMAIN}/login?client_id={COGNITO_APP_CLIENT_ID}&response_type=code&scope=email+openid+profile&redirect_uri={COGNITO_CALLBACK_URL}"

def get_cognito_logout_url():
    """Generate the Cognito hosted UI logout URL"""
    return f"https://{COGNITO_DOMAIN}/logout?client_id={COGNITO_APP_CLIENT_ID}&logout_uri={COGNITO_LOGOUT_URL}"

async def exchange_code_for_tokens(code: str) -> Dict:
    """Exchange authorization code for tokens"""
    try:
        response = cognito_idp.initiate_auth(
            ClientId=COGNITO_APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': code,  # In a real app, this would be the authorization code
                'PASSWORD': 'dummy_password'  # In a real app, this would not be needed
            }
        )
        
        # In a real implementation, you would use the admin_initiate_auth or initiate_auth
        # with the correct auth flow and parameters
        
        # This is a placeholder for demonstration
        return {
            "id_token": "dummy_id_token",
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token",
            "expires_in": 3600
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to exchange code for tokens: {str(e)}"
        )

async def verify_cognito_token(token: str) -> Dict:
    """Verify a Cognito JWT token"""
    try:
        # In a real implementation, you would verify the token with Cognito
        # This is a placeholder for demonstration
        return {
            "sub": "dummy_user_id",
            "email": "user@example.com",
            "name": "Test User"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
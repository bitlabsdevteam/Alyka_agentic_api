# src/agentic_api/middleware.py

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from .auth import get_current_user
import jwt
import os
from typing import List, Callable, Optional

# Load JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

class AuthMiddleware:
    """Middleware for handling authentication"""
    
    def __init__(self, exempt_paths: List[str] = None):
        """Initialize the middleware with paths that are exempt from authentication"""
        self.exempt_paths = exempt_paths or [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/auth/login",
            "/auth/callback",
            "/auth/logout"
        ]
    
    async def __call__(self, request: Request, call_next: Callable):
        """Process the request and enforce authentication"""
        # Check if the path is exempt from authentication
        if any(request.url.path.startswith(path) for path in self.exempt_paths):
            return await call_next(request)
        
        # Get the authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Not authenticated"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Extract the token
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                    headers={"WWW-Authenticate": "Bearer"}
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify the token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.state.user = payload
        except jwt.PyJWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"},
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Continue processing the request
        return await call_next(request)


def get_auth_middleware(exempt_paths: Optional[List[str]] = None) -> AuthMiddleware:
    """Factory function to create an instance of AuthMiddleware"""
    return AuthMiddleware(exempt_paths=exempt_paths)
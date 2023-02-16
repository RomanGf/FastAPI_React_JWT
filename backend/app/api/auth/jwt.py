from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from pydantic import ValidationError
from services.user_services import UserService
from core.security import create_access_token, create_refresh_token
from schemas.auth_schema import TokenSchema
from schemas.user_schema import UserOut
from models.user_model import User
from api.dependencies.user_deps import get_current_user
from core.config import settings
from schemas.auth_schema import TokenPayload
from jose import jwt


auth_route = APIRouter()

@auth_route.post("/login", summary="Create access and refresh token for user",
                 response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, 
                                          password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    return {
        'access_token': create_access_token(user.user_id),
        'refresh_token': create_refresh_token(user.user_id)
    }

@auth_route.post("/test-token", summary="Test is the access token is valid",
                 response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)):
    return user


@auth_route.post("/refresh", summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = await UserService.get_user_by_id(token_data.sub)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )
    
    return {
        'access_token': create_access_token(user.user_id),
        'refresh_token': create_refresh_token(user.user_id)
    }
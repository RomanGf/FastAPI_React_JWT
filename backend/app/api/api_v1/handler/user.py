import pymongo

from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserAuth, UserOut
from services.user_services import UserService


user_router = APIRouter()

@user_router.post("/create", summary="Create new User", response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )
from fastapi import APIRouter
from api.api_v1.handler.user import user_router
from api.api_v1.handler.todo import todo_router
from api.auth.jwt import auth_route
router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_route, prefix="/auth", tags=["auth"])
router.include_router(todo_router, prefix="/todo", tags=["todo"])
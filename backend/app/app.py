import uvicorn


from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.user_model import User
from models.todo_models import Todo
from core.config import settings
from api.api_v1.example_router import router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
) 

@app.on_event("startup")
async def app_init():
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).fast_db

    await init_beanie(
        database= db_client,
        document_models= [
        User,
        Todo
        ],

    )

app.include_router(router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    uvicorn.run("app:app", host='127.0.0.1', port=8000, reload=True)
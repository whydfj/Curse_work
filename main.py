from fastapi import FastAPI, HTTPException
from authx import AuthX, AuthXConfig
from pydantic import BaseModel, Field
from sqlalchemy import text

from data_base_work import engine, new_session


#pydantic схемы
class User_Schema(BaseModel):
    username: str = Field(max_length=60)
    password: str = Field(max_length=20)


config = AuthXConfig()

config.JWT_ACCESS_COOKIE_NAME = "aboba"
config.JWT_SECRET_KEY = "test-secret-key"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


app = FastAPI()


@app.post("/login_by_admin")
async def login_by_admin(user: User_Schema):
    with new_session() as session:
        # ПРАВИЛЬНО: параметры как словарь вторым аргументом
        result = session.execute(text("SELECT * FROM Users WHERE username = :username"), {"username": user.username})
        return result
        #сам с этим говном разбирайся

@app.get("/")
def main_page():
    p = 0
    if p == 2:
        return {"qq": 1}

    raise HTTPException(status_code=404, detail="не найдено(")


@app.get("/data")
def all_data():
    return {"message": "Типа вывелась вся бд"}


@app.get("/get")
def all():
    return {"message": "Типа вывелась вся бд"}


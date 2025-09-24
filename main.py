#Давид, "/login" - он будет для всех, в нем надо будет реализовать проверку по роли, подходит нам чел или нет
#/createUser это будет для админа, чтобы он там могут создавать пользователей или других админов
#/mainWindowUser это будет основное, где будет таблица с тасками, а переход по ним будет во всплывающем окне))
#userSettings это будет окно с настройками веб приложения
#если будет что добавить, то добавляй, принцип я думаю ты поймешь, каждая такая функция должна быть как отдельный файл, пока не создаю отдельный файл, чтобы ты мог что-то изменить и добавить без гемора
#Основной функционал:
#
#1. Аутентификация:
#— Простая система логина/пароля
#— Две роли: руководитель и сотрудник
#— Сессионная аутентификация
#
#2. Руководитель может:
#— Создавать карточки сотрудников
#— Добавлять задачи для развития
#— Устанавливать дедлайны
#— Просматривать прогресс выполнения
#— Оставлять комментарии
#
#3. Сотрудник может:
#— Видеть список своих задач
#— Отмечать прогресс выполнения (0-100%)
#— Добавлять комментарии к задачам
#— Прикреплять файлы (опционально)
from fastapi import FastAPI, HTTPException
from authx import AuthX, AuthXConfig
from pydantic import BaseModel, Field


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



@app.post("/login/")
def login_by_admin():
    return {"ЛОГИН ДЛЯ ВСЕХ"}


@app.get("/createUser/")
def create_user():
    return{"Администратор создает здесь пользователей"}


@app.get("/userSettings/")
def login_by_admin():
    return {"ЛОГИН ДЛЯ ВСЕХ"}

@app.get("/mainWindowUser/")
def main_window_user():
    return {"Всякие таски, хуяски"}

@app.get("/")
def main_page():
    p = 0
    if p == 2:
        return {"qq": 1}

    raise HTTPException(status_code=404, detail="не найдено(")


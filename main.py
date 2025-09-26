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
"""Давид, я сделал поддержку ORM нашей Бд, пример работы(файл data_base_work):
all_users = session.query(User).all()
for user in all_users:
    if(user.role == "manager"):
        print(f"{user.username} {user.password_hash} {user.created_at}")

создал файл Password_hash.py, он как раз будет высчитывать хэш для нашего приложения (Хэширование с помощью BLAKE2b) почитай в инетике))
пароль для админа - password
пароль для user 123456
Но они понятное дело хранятся как захэшированные

далее я баловался с ии и сделал database_shortcat.py(очень удобно, буду сам дополнять этот файл, чтобы можно было быстро, что-то использовать из бд)
сейчас расскажу про методы в нем:

get_all_users - получить всех юзеров
get_user_by_username(username) - получить юзера по юзернейму
get_tasks_by_user(user_id) - получить юзеров по таску(задаче)
create_user(username, password_hash, role, name, surname) - создать юзера с такими полями(поле даты и времени обновляется при создании автоматически)
create_task(employee_id, title, description, status="running", progress=0) - создать таск для определенного юзера
get_login(username,password) (уже сам делал) - команда для авторизации пользователя(или админа).
"""

from fastapi import FastAPI, HTTPException, Response
from authx import AuthX, AuthXConfig
from pydantic import BaseModel, Field
from sqlalchemy import select

from DB_SQLite.data_base_work import new_session, Users

from DB_SQLite.database_shortcat import DatabaseManager


#pydantic схемы
class User_Login_Schema(BaseModel):
    username: str = Field(max_length=60)
    password: str = Field(max_length=20)


class User_Create_Schema(BaseModel):
    username: str = Field(max_length=60)
    password: str = Field(max_length=20)
    role: str = Field(max_length=10)
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)



config = AuthXConfig()

config.JWT_ACCESS_COOKIE_NAME = "aboba"
config.JWT_SECRET_KEY = "test-secret-key"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


app = FastAPI()

methods = DatabaseManager()


@app.post("/login")
def login(user: User_Login_Schema, response: Response):
    # with new_session() as session:
    #     new_user = session.execute(select(Users).where(Users.username == user.username)).scalar_one_or_none()
    #     if new_user is None:
    #         raise HTTPException(status_code=409, detail="User is not found")
    #     return {"message": "Пользователь найден", "sss": new_user}

    t_user = DatabaseManager.get_login("admin", "password")
    if t_user is None:
        raise HTTPException(status_code=409, detail="User is not found")

    token = security.create_access_token(uid=str(t_user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"message": "Пользователь найден", "sss": t_user, "token": token}


@app.post("/createUser")
def create_user(user: User_Create_Schema):
    User = methods.get_user_by_username(user.username)
    if User is None:
        methods.create_user(user.username, user.password, user.role, user.name, user.surname)
        return {"status": True, "message": "Пользователь создан успешно!"}
    else:
        raise HTTPException(status_code=404, detail="Пользователь с таким именем уже есть!")


@app.get("/userSettings")
def login_by_admin():
    return {"ЛОГИН ДЛЯ ВСЕХ"}


@app.get("/mainWindowUser")
def main_window_user():
    return {"Всякие таски, хуяски"}


@app.get("/")
def main_page():
    p = 0
    if p == 2:
        return {"qq": 1}

    raise HTTPException(status_code=404, detail="не найдено(")


print(DatabaseManager.get_login("admin", "password"))
user = User_Login_Schema(username="admin", password="12345")
with new_session() as session:
    print(session.execute(select(Users)).all())

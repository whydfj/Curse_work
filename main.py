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
import uvicorn
from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from fastapi.params import Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from starlette.responses import RedirectResponse

from DB_SQLite.data_base_work import new_session, Users

from DB_SQLite.database_shortcat import DatabaseManager as methods



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


class User_Found_and_Delete_Schema(BaseModel):
    username: str = Field(max_length=60)


config = AuthXConfig()

config.JWT_ACCESS_COOKIE_NAME = "aboba"
config.JWT_SECRET_KEY = "test-secret-key"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False  # 👈 отключаем CSRF проверку

security = AuthX(config=config)


app = FastAPI()


def is_manager(current_user: dict = Depends(security.access_token_required)):
    """
    Получение информации о текущем пользователе
    """
    user_id = int(dict(current_user)["sub"])

    with new_session() as session:
        users_role = session.execute(select(Users.role).where(Users.id == user_id))

    return users_role.scalar() == "manager"


@app.post("/login")
def login(user: User_Login_Schema, response: Response):
    # with new_session() as session:
    #     new_user = session.execute(select(Users).where(Users.username == user.username)).scalar_one_or_none()
    #     if new_user is None:
    #         raise HTTPException(status_code=409, detail="User is not found")
    #     return {"message": "Пользователь найден", "sss": new_user}
    t_user = methods.get_login(user.username, user.password)
    if t_user is None:
        raise HTTPException(status_code=409, detail="User is not found")

    token = security.create_access_token(uid=str(t_user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"message": "Пользователь найден", "sss": t_user, "token": token}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME, secure=False, httponly=True, samesite="lax")
    return {"message": "Вы успешно вышли из системы", "status": True}


@app.post("/createUser")
def create_user(user: User_Create_Schema, current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    with new_session() as session:
        users_role = session.execute(select(Users.role).where(Users.id == user_id))
    users_role = users_role.scalar()
    User = methods.get_user_by_username(user.username)
    if users_role != "manager":
        raise HTTPException(status_code=401, detail="Извините, пользователей может создавать только менеджер!")
    if User is None:
        if len(user.password) < 4:
            raise HTTPException(status_code=404, detail="Длина пароля должна быть хотя бы 4")
        methods.create_user(user.username, user.password, user.role, user.name, user.surname)
        return {"status": True, "message": "Пользователь создан успешно!"}
    else:
        raise HTTPException(status_code=405, detail="Пользователь с таким именем уже есть!")


@app.post("/found")
def found_user(user: User_Found_and_Delete_Schema):
    User = methods.get_user_by_username(user.username)
    if User is not None:
        methods.get_user_by_username(user.username)
        return {"status": True, "message": "Пользователь найден" , "name_user": User.name,"surname_user": User.surname,"role_user":User.role,"created_at": User.created_at}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.delete("/found/delete")
def delete_user(user: User_Found_and_Delete_Schema):
    User = methods.get_user_by_username(user.username)
    if User is not None:
        methods.delete_user(user.username)
        return {"status": True, "message": "Пользователь удален"}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.post("/found/show_all")
def show_all():
    if methods.number_of_all_users() > 0:
        return methods.get_all_users()
    return {"status" : True, "message": "Пользователи не найдены"}


@app.get("/userSettings")
def UserSettings():
    return {"ЛОГИН ДЛЯ ВСЕХ"}


@app.get("/mainWindowUser")
def main_window_user():
    return {"Всякие таски, хуяски"}


@app.get("/")
def main_page():
    return RedirectResponse(url="/login")
    #p = 0
    #if p == 2:
    #    return {"qq": 1}
#
    #raise HTTPException(status_code=404, detail="не найдено(")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)


#with new_session() as session:
#    print(session.execute(select(Users)).all())



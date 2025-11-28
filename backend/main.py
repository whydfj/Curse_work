"""
Давид, "/login" - он будет для всех, в нем надо будет реализовать проверку по роли, подходит нам чел или нет
/createUser это будет для админа, чтобы он там могут создавать пользователей или других админов
/mainWindowUser это будет основное, где будет таблица с тасками, а переход по ним будет во всплывающем окне))
userSettings это будет окно с настройками веб приложения
если будет что добавить, то добавляй, принцип я думаю ты поймешь, каждая такая функция должна быть как отдельный файл,
пока не создаю отдельный файл, чтобы ты мог что-то изменить и добавить без гемора
Основной функционал:

1. Аутентификация:
— Простая система логина/пароля
— Две роли: руководитель и сотрудник
— Сессионная аутентификация

2. Руководитель может:
— Создавать карточки сотрудников
— Добавлять задачи для развития
— Устанавливать дедлайны
— Просматривать прогресс выполнения
— Оставлять комментарии

3. Сотрудник может:
— Видеть список своих задач
— Отмечать прогресс выполнения (0-100%)
— Добавлять комментарии к задачам
— Прикреплять файлы (опционально)
Давид, я сделал поддержку ORM нашей Бд, пример работы(файл data_base_work):
all_users = session.query(User).all()
for user in all_users:
    if(user.role == "manager"):
        print(f"{user.username} {user.password_hash} {user.created_at}")

создал файл Password_hash.py, он как раз будет высчитывать хэш для нашего приложения (Хэширование с помощью BLAKE2b)
 почитай в инетике))
пароль для админа - password
пароль для user 123456
Но они понятное дело хранятся как захэшированные далее я баловался с ии и сделал database_shortcat.py(очень удобно, буду
 сам дополнять этот файл, чтобы можно было быстро,что-то использовать из бд) сейчас расскажу про методы в нем:

get_all_users - получить всех юзеров
get_user_by_username(username) - получить юзера по юзернейму
get_tasks_by_user(user_id) - получить юзеров по таску(задаче)
create_user(username, password_hash, role, name, surname) - создать юзера с такими полями(поле даты и времени
обновляется при создании автоматически)
create_task(employee_id, title, description, status="running", progress=0) - создать таск для определенного юзера
get_login(username,password) (уже сам делал) - команда для авторизации пользователя(или админа).fd
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from backend.api import manager, user, admin
from backend.api.ai_assistant import ai_chat

app = FastAPI()
app.include_router(admin.router)
app.include_router(manager.router)
app.include_router(user.router)
app.include_router(ai_chat.router)


@app.get("/userSettings", tags=["UI"])
def UserSettings():
    return {"ЛОГИН ДЛЯ ВСЕХ"}


@app.get("/mainWindowUser", tags=["UI"])
def main_window_user():
    return {""}


@app.get("/", tags=["UI"])
def main_page():
    return RedirectResponse(url="/login")


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

# with new_session() as session:
#    print(session.execute(select(Users)).all())

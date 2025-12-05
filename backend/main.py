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
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from backend.api import manager, user, admin
from backend.api.ai_assistant import ai_chat
from authx.exceptions import MissingTokenError

app = FastAPI()

# CORS — правильно
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Статика
app.mount("/static", StaticFiles(directory="static"), name="static")


# ЕДИНСТВЕННЫЙ корневой роутер — отдаём index.html
@app.get("/", tags=["UI"])
def main_page():
    return RedirectResponse(url="/static/index.html")

# Обработка ошибки токена

@app.exception_handler(MissingTokenError)
async def missing_token_handler(request, exc: MissingTokenError):
    raise HTTPException(
        status_code=401,
        detail="Not authenticated: access token is missing",
    )

# Подключаем API с префиксом /api
app.include_router(admin.router, prefix="/api")
app.include_router(manager.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(ai_chat.router, prefix="/api")


# Вспомогательные эндпоинты (если нужны)
@app.get("/userSettings", tags=["UI"])
def user_settings():
    return {"message": "ЛОГИН ДЛЯ ВСЕХ"}


@app.get("/mainWindowUser", tags=["UI"])
def main_window_user():
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
# with new_session() as session:
#    print(session.execute(select(Users)).all())

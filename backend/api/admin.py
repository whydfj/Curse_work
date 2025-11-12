from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks
from sqlalchemy import select, update, delete

from backend.DB_SQLite.data_base_work import new_session, Users, Tasks
from backend.api.manager import is_manager
from backend.core.security import security
from backend.schemas.tasks import Task_Schema, Task_Set_Schema, Task_Delete_Schema, Deadline_Set_Schema
from backend.schemas.users import User_Create_Schema, User_Found_and_Delete_Schema
from backend.DB_SQLite.database_shortcat import DatabaseManager as methods

router = APIRouter()

async def is_admin(user_id):
    async with new_session() as session:
        users_role = await session.execute(
            select(Users.role)
            .where(Users.id == user_id)  # type: ignore
        )
        return users_role.scalar_one_or_none()

@router.post("/create_user", tags=["User Management"])
async def create_user(background_tasks: BackgroundTasks, user: User_Create_Schema, current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    role = await is_admin(user_id)
    if role != "admin":
        raise HTTPException(status_code=401, detail="Извините, пользователей может создавать только администратор!")
    existing_user = await methods.get_user_by_username_or_email(user.username, user.email_user)

    if existing_user:
        raise HTTPException(status_code=405, detail="Пользователь с таким именем или email уже существует!")
    if len(user.password) < 4:
        raise HTTPException(status_code=400, detail="Длина пароля должна быть хотя бы 4")
    new_user = await methods.create_user(user.username, user.password, user.role, user.name, user.surname, user.email_user)

    background_tasks.add_task(
        methods.send_registration_email,
        user.email_user,
        user.username,
        user.password
    )

    return {
        "status": True,
        "message": "Пользователь создан успешно! Уведомление отправлено на email."
    }

@router.delete("/found/delete", tags=["User Management"])
async def delete_user(user: User_Found_and_Delete_Schema, current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    role = await is_admin(user_id)
    if role != "admin":
        raise HTTPException(status_code=401, detail="Извините, пользователей может удалять только администратор!")
    User = await methods.get_user_by_username(user.username)
    if User is not None:
        await methods.delete_user(user.username)
        return {"status": True, "message": "Пользователь удален"}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
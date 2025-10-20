from fastapi import HTTPException, Response, APIRouter, Depends
from sqlalchemy import select, update

from backend.DB_SQLite.data_base_work import new_session, Tasks
from backend.core.security import security, config
from backend.schemas.tasks import Progress_Update_Schema
from backend.schemas.users import User_Login_Schema, User_Found_and_Delete_Schema, Comment_Schema
from backend.DB_SQLite.database_shortcat import DatabaseManager as methods


router = APIRouter()


@router.post("/login", tags=["Authentication"])
async def login(user: User_Login_Schema, response: Response):
    # with new_session() as session:
    #     new_user = session.execute(select(Users).where(Users.username == user.username)).scalar_one_or_none()
    #     if new_user is None:
    #         raise HTTPException(status_code=409, detail="User is not found")
    #     return {"message": "Пользователь найден", "sss": new_user}
    t_user = await methods.get_login(user.username, user.password)
    if t_user is None:
        raise HTTPException(status_code=409, detail="User is not found")

    token = security.create_access_token(uid=str(t_user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"message": "Пользователь найден", "sss": t_user, "token": token}


@router.post("/logout", tags=["Authentication"])
async def logout(response: Response):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME, secure=False, httponly=True, samesite="lax")
    return {"message": "Вы успешно вышли из системы", "status": True}


@router.post("/found", tags=["User Management"])
async def found_user(user: User_Found_and_Delete_Schema):
    User = await methods.get_user_by_username(user.username)
    if User is not None:
        return {"status": True, "message": "Пользователь найден",
                "name_user": User.name, "surname_user": User.surname,
                "role_user": User.role, "created_at": User.created_at}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.delete("/found/delete", tags=["User Management"])
async def delete_user(user: User_Found_and_Delete_Schema):
    User = await methods.get_user_by_username(user.username)
    if User is not None:
        await methods.delete_user(user.username)
        return {"status": True, "message": "Пользователь удален"}
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


@router.get("/get_current_user", tags=["User Management"])
async def current_user(current_user: dict = Depends(security.access_token_required)):
    users_id = int(dict(current_user)["sub"])
    user = await methods.get_user_by_id(users_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Войдите для того чтобы увидеть свой профиль")
    return user


@router.get("/get_my_tasks", tags=["Task Management"])
async def get_my_tasks(current_user: dict = Depends(security.access_token_required)):
    async with new_session() as session:
        user_id = int(dict(current_user)["sub"])
        user_tasks = await session.execute(
            select(Tasks)
            .where(Tasks.employee_id == user_id)
        )
        return user_tasks.scalars().all()


@router.patch("/tasks/{task_id}/progress", tags=["Task Management"])
async def update_progress(progress_data: Progress_Update_Schema,
                    current_user: dict = Depends(security.access_token_required)):
    """Обновить прогресс выполнения задачи"""
    user_id = int(dict(current_user)["sub"])
    async with new_session() as session:
        task = await session.execute(select(Tasks).where(
            Tasks.title == progress_data.task_title,
            Tasks.employee_id == user_id
        ))
        task = task.scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=404, detail="Задача не найдена")

        await session.execute(
            update(Tasks)
            .where(Tasks.title == progress_data.task_title)
            .values(progress=progress_data.progress)
        )
        await session.commit()
        return {"message": "Прогресс обновлен", "progress": progress_data.progress}


@router.post("/add_new_comment")
async def add_new_comment(new_comment: Comment_Schema, current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    new_comment = await methods.add_comment(
        task_id=new_comment.task_id,
        user_id=user_id,
        attached_file=new_comment.attached_file,
        text=new_comment.text
    )
    if new_comment is None:
        raise HTTPException(status_code=403, detail="Вам не доступна данная функция")

    return {"status": True, "message": "Комментарий успешно добавлен"}



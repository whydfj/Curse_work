from fastapi import Depends, HTTPException, APIRouter, BackgroundTasks
from sqlalchemy import select, update, delete

from backend.DB_SQLite.data_base_work import new_session, Users, Tasks
from backend.core.security import security
from backend.schemas.tasks import Task_Schema, Task_Set_Schema, Task_Delete_Schema, Deadline_Set_Schema
from backend.schemas.users import User_Create_Schema
from backend.DB_SQLite.database_shortcat import DatabaseManager as methods

router = APIRouter()


async def is_manager(user_id):
    async with new_session() as session:
        users_role = await session.execute(
            select(Users.role)
            .where(Users.id == user_id)  # type: ignore
        )
        return users_role.scalar_one_or_none()


@router.post("/add_task", tags=["Task Management"])
async def add_task(task: Task_Schema):
    async with new_session() as session:
        # Получаем ID пользователя
        user_id = await methods.get_user_id_by_username2(task.username)
        if not user_id:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Проверяем, существует ли уже задача с таким названием у этого пользователя
        existing_task = await session.execute(
            select(Tasks).where(
                Tasks.title == task.title,
                Tasks.employee_id == user_id  # type: ignore
            )
        )
        existing_task = existing_task.scalar_one_or_none()

        if existing_task is None:
            new_task = await methods.create_task_with_deadline(user_id, task.title, task.description, task.deadline)
            await session.commit()
            return {"message": "Task added", "task": new_task}

        raise HTTPException(status_code=400, detail="Задача уже существует!")


@router.patch("/set_task", tags=["Task Management"])
async def set_task(new_task: Task_Set_Schema):
    async with new_session() as session:
        t = await session.execute(
            select(Tasks)
            .where(Tasks.employee_id == await methods.get_user_id_by_username(new_task.username) # type: ignore
                   , Tasks.title == new_task.title)
        )

        t = t.scalar_one_or_none()
        if t is None:
            raise HTTPException(status_code=404, detail="Задача не найдена, проверьте никнейм или задачу")

        await session.execute(
            update(Tasks)
            .where(Tasks.employee_id == await methods.get_user_id_by_username(new_task.username) # type: ignore
                   , Tasks.title == new_task.title)
            .values(title=new_task.new_title, description=new_task.new_description))
        await session.commit()
        return {"message": "Задача успешно изменена!", "status": True}


@router.delete("/delete_task", tags=["Task Management"])
async def delete_task(task: Task_Delete_Schema, current_user: dict = Depends(security.access_token_required)):
    async with (new_session() as session):

        role = await is_manager(int(dict(current_user)["sub"]))

        if role != "manager" and role != "admin":
            raise HTTPException(status_code=403, detail="У вас нет доступа к данной функции")

        t = await session.execute(
            select(Tasks)
            .where(Tasks.employee_id == await methods.get_user_id_by_username(task.username)  # type: ignore
                   , Tasks.title == task.title)
        )
        t = t.scalars().all()
        if t is None:
            raise HTTPException(status_code=404, detail="Задача не найдена, проверьте никнейм или задачу")

        await session.execute(
            delete(Tasks)
            .where(Tasks.employee_id == await methods.get_user_id_by_username(task.username)  # type: ignore
                   , Tasks.title == task.title)
        )
        # Тест с g
        await session.commit()
        return {"message": "Задача успешно удалена!", "status": True}


@router.get("/get_user_tasks/{username}", tags=["Task Management"])
async def get_user_tasks(username: str):
    user_tasks = await methods.get_all_users_tasks(username)
    if user_tasks is None:
        raise HTTPException(status_code=404, detail="У пользователя нет действующих задач")
    return user_tasks


@router.get("/get_all_tasks")
async def get_all_tasks(current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    role = await is_manager(user_id)
    if role != "manager" and role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    async with new_session() as session:
        all_tasks = await session.execute(
            select(Tasks)
        )
        return all_tasks.scalars().all()


@router.patch("/update_deadline")
async def update_deadline(deadline: Deadline_Set_Schema, current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    role = await is_manager(user_id)
    if role != "manager" and role != "admin":
        raise HTTPException(status_code=403, detail="Извините, у вас нет доступа к данной функции")
    async with new_session() as session:
        await session.execute(
            update(Tasks)
            .where(Tasks.id == deadline.task_id)
            .values(deadline=deadline.new_deadline)
        )
        await session.commit()

        return {"status": True, "message": "Дедлайн успешно обновлен"}


@router.get("/found/show_all", tags=["User Management"])
async def show_all():
    if await methods.number_of_all_users() > 0:
        res = await methods.get_all_users()
        return res
    raise HTTPException(status_code=404, detail="Действующих пользователей нет")

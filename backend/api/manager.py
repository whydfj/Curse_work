from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update, delete

from backend.DB_SQLite.data_base_work import new_session, Users, Tasks
from backend.core.security import security
from backend.schemas.tasks import Task_Schema, Task_Set_Schema, Task_Delete_Schema, Deadline_Set_Schema
from backend.schemas.users import User_Create_Schema
from backend.DB_SQLite.database_shortcat import DatabaseManager as methods


router = APIRouter()


def is_manager(user_id):
    """
    Получение информации о текущем пользователе
    """

    with new_session() as session:
        users_role = session.execute(select(Users.role).where(Users.id == user_id))  # type: ignore

    return users_role.scalar()


@router.post("/create_user", tags=["User Management"])
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


@router.post("/add_task", tags=["Task Management"])
async def add_task(task: Task_Schema):
    with new_session() as session:
        # Получаем ID пользователя
        user_id = methods.get_user_id_by_username2(task.username)
        if not user_id:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        # Проверяем, существует ли уже задача с таким названием у этого пользователя
        existing_task = session.execute(
            select(Tasks).where(
                Tasks.title == task.title,
                Tasks.employee_id == user_id  # type: ignore
            )
        ).scalar_one_or_none()

        if existing_task is None:
            new_task = methods.create_task_with_deadline(user_id, task.title, task.description, task.deadline)
            session.commit()
            return {"message": "Task added", "task": new_task}

        raise HTTPException(status_code=400, detail="Задача уже существует!")


@router.patch("/set_task", tags=["Task Management"])
def set_task(new_task: Task_Set_Schema):
    with (new_session() as session):
        t = session.execute(select(Tasks)
                            .where(Tasks.employee_id == methods.get_user_id_by_username(new_task.username) # type: ignore
                                   , Tasks.title == new_task.title)
                            )

        t = t.scalar_one_or_none()
        if t is None:
            raise HTTPException(status_code=404, detail="Задача не найдена, проверьте никнейм или задачу")

        session.execute(update(Tasks).where(Tasks.employee_id == methods.get_user_id_by_username(new_task.username)
                                            , Tasks.title == new_task.title)
                        .values(title=new_task.new_title, description=new_task.new_description))
        session.commit()
        return {"message": "Задача успешно изменена!", "status": True}


@router.delete("/delete_task", tags=["Task Management"])
def delete_task(task: Task_Delete_Schema, current_user: dict = Depends(security.access_token_required)):
    with (new_session() as session):

        role = is_manager(int(dict(current_user)["sub"]))

        if role != "manager":
            raise HTTPException(status_code=403, detail="У вас нет доступа к данной функции")

        t = session.execute(select(Tasks)
                            .where(Tasks.employee_id == methods.get_user_id_by_username(task.username)  # type: ignore
                                   , Tasks.title == task.title)
                            ).scalars().all()
        if t is None:
            raise HTTPException(status_code=404, detail="Задача не найдена, проверьте никнейм или задачу")

        session.execute(delete(Tasks)
                        .where(Tasks.employee_id == methods.get_user_id_by_username(task.username)  # type: ignore
                               , Tasks.title == task.title)
                        )
        # Тест с g
        session.commit()
        return {"message": "Задача успешно удалена!", "status": True}


@router.get("/get_user_tasks/{username}", tags=["Task Management"])
def get_user_tasks(username: str):
    user_tasks = methods.get_all_users_tasks(username)
    if user_tasks is None:
        raise HTTPException(status_code=404, detail="У пользователя нет действующих задач")
    return user_tasks


@router.get("/get_all_tasks")
def get_all_tasks(current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    role = is_manager(user_id)
    if role != "manager":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    with new_session() as session:
        all_tasks = session.execute(
            select(Tasks)
        ).scalars().all()

        return all_tasks


@router.patch("/update_deadline")
def update_deadline(deadline: Deadline_Set_Schema, current_user: dict = Depends(security.access_token_required)):
    user_id = int(dict(current_user)["sub"])
    role = is_manager(user_id)
    if role != "manager":
        raise HTTPException(status_code=403, detail="Извините, у вас нет доступа к данной функции")
    with new_session() as session:
        session.execute(
            update(Tasks)
            .where(Tasks.id == deadline.task_id)
            .values(deadline=deadline.new_deadline)
        )
        session.commit()

        return {"status": True, "message": "Дедлайн успешно обновлен"}


@router.get("/found/show_all", tags=["User Management"])
def show_all():
    if methods.number_of_all_users() > 0:
        return methods.get_all_users()
    raise HTTPException(status_code=404, detail="Действующих пользователей нет")

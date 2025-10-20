from sqlalchemy import select

from backend.DB_SQLite.data_base_work import Users, Tasks, Comment, new_session
from Password_hash import passwordHash


class DatabaseManager:
    @staticmethod
    async def get_all_users():
        async with new_session() as s:
            res = await s.execute(
                select(Users)
            )
            return res.scalars().all()

    @staticmethod
    async def get_user_by_username(username):
        async with new_session() as s:
            res = await s.execute(
                select(Users)
                .where(Users.username == username)  # type: ignore
            )
            return res.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(id: int):
        async with (new_session() as s):
            user = await s.execute(
                select(Users)
                .where(Users.id == id)
            )
            user = user.scalar_one_or_none()
            if user is None:
                return None
            return user

    @staticmethod
    async def get_user_id_by_username(username):
        async with new_session() as s:
            res = await s.execute(
                select(Users.id)
                .where(Users.username == username)  # type: ignore
            )
            res = res.scalar()
            return res

    @staticmethod
    async def get_user_id_by_username2(username):
        async with new_session() as s:
            res = await s.execute(
                select(Users.id).where(Users.username == username)  # type: ignore
            )
            res = res.scalar()
            return res

    @staticmethod
    async def get_tasks_by_user(user_id):
        async with new_session() as s:
            res = await s.execute(
                select(Tasks)
                .where(Tasks.employee_id == user_id)  # type: ignore
            )
            res = res.scalars().all()
            return res

    @staticmethod
    async def create_user(username, password_hash, role, name, surname):
        new_user = Users(
            username=username,
            password_hash=passwordHash.blake2b_hash(password_hash),
            role=role,
            name=name,
            surname=surname
        )
        async with new_session() as s:
            s.add(new_user)
            await s.commit()
            return new_user

    @staticmethod
    async def create_task(employee_id, title, description, status="running", progress=0):
        new_task = Tasks(
            employee_id=employee_id,
            title=title,
            description=description,
            status=status,
            progress=progress
        )
        async with new_session() as s:
            s.add(new_task)
            await s.commit()
            return new_task

    @staticmethod
    async def create_task_with_deadline(employee_id, title, description, deadline, status="running", progress=0):
        new_task = Tasks(
            employee_id=employee_id,
            title=title,
            description=description,
            status=status,
            progress=progress,
            deadline=deadline
        )
        async with new_session() as s:
            s.add(new_task)
            await s.commit()
            return new_task

    @staticmethod
    async def get_login(username, password):
        password_hash = passwordHash.blake2b_hash(password)
        async with new_session() as s:
            result = await s.execute(
                select(Users).where(
                    Users.username == username,
                    Users.password_hash == password_hash
                )
            )
            return result.scalar_one_or_none()

    @staticmethod
    async def delete_user(username):
        async with new_session() as s:
            user_to_delete = await s.execute(
                select(Users)
                .where(Users.username == username)  # type: ignore
            )
            user_to_delete = user_to_delete.scalar_one_or_none()
            if user_to_delete is None:
                return None
            await s.delete(user_to_delete)
            await s.commit()
            return True

    @staticmethod
    async def number_of_all_users():
        async with new_session() as s:
            result = await s.execute(select(Users))
            return len(result.scalars().all())

    @staticmethod
    async def get_all_users_tasks(username: str):
        async with new_session() as t_session:
            user_id = await DatabaseManager().get_user_id_by_username(username)

            users_tasks = await t_session.execute(
                select(Tasks).where(Tasks.employee_id == user_id)  # type: ignore
            )

            return users_tasks.scalars().all()

    @staticmethod
    async def add_comment(task_id: int, user_id: int, text: str, attached_file=None):
        async with new_session() as s:
            user = await s.execute(
                select(Users)
                .where(Users.id == user_id)
            )
            user = user.scalar_one_or_none()
            if user is None:
                return None

            task = await s.execute(
                select(Tasks)
                .where(Tasks.id == task_id)
            )
            task = task.scalar_one_or_none()
            if task is None:
                return None

            if user.role != "manager":
                if task.employee_id != user_id:
                    return None
            new_comment = Comment(
                task_id=task_id,
                text=text,
                user_id=user_id,
                attached_file=attached_file,
            )
            s.add(new_comment)
            await s.commit()
            return new_comment

    @staticmethod
    async def add_comment2(user_id, text, task_id):
        async with new_session() as s:
            user = await s.execute(
                select(Users)
                .where(user_id == Users.id)  # type: ignore
            )
            user = user.scalar_one_or_none()
            task = await s.execute(
                select(Tasks)
                .where(task_id == Tasks.id)  # type: ignore
            )
            task = task.scalar_one_or_none()
            if user_id is None:
                return None
            if task is None:
                return None

            if user.role != "manager":
                if task.employee_id != user_id:
                    return None

            new_comment = Comment(
                task_id=task_id,
                text=text,
                user_id=user_id
            )

            s.add(new_comment)
            await s.commit()
            return new_comment

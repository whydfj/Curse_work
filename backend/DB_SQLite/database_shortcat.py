from sqlalchemy import select

from backend.DB_SQLite.data_base_work import session, Users, Tasks, Comment, new_session
from Password_hash import passwordHash


class DatabaseManager:
    @staticmethod
    def get_all_users():
        with new_session() as s:
            return s.execute(
                select(Users)
            ).scalars().all()


    @staticmethod
    def get_user_by_username(username):
        with new_session() as s:
            return s.execute(
                select(Users)
                .where(Users.username == username)  # type: ignore
            ).scalar_one_or_none()

    @staticmethod
    def get_user_by_id(id: int):
        with new_session() as s:
            user = s.execute(
                select(Users)
                .where(Users.id == id)
            ).scalar_one_or_none()
            if user is None:
                return None
            return user

    @staticmethod
    def get_user_id_by_username(username):
        with new_session() as s:
            return s.execute(
                select(Users.id)
                .where(Users.username == username)  # type: ignore
            ).scalar()

    @staticmethod
    def get_user_id_by_username2(username):
        with new_session() as s:
            return s.execute(
                select(Users.id).where(Users.username == username)  # type: ignore
            ).scalar()

    @staticmethod
    def get_tasks_by_user(user_id):
        with new_session() as s:
            return s.execute(
                select(Tasks)
                .where(Tasks.employee_id == user_id)  # type: ignore
            ).scalars().all()

    @staticmethod
    def create_user(username, password_hash, role, name, surname):
        new_user = Users(
            username=username,
            password_hash=passwordHash.blake2b_hash(password_hash),
            role=role,
            name=name,
            surname=surname
        )
        with new_session() as s:
            s.add(new_user)
            s.commit()
            return new_user

    @staticmethod
    def create_task(employee_id, title, description, status="running", progress=0):
        new_task = Tasks(
            employee_id=employee_id,
            title=title,
            description=description,
            status=status,
            progress=progress
        )
        with new_session() as s:
            s.add(new_task)
            s.commit()
            return new_task

    @staticmethod
    def create_task_with_deadline(employee_id, title, description, deadline, status="running", progress=0):
        new_task = Tasks(
            employee_id=employee_id,
            title=title,
            description=description,
            status=status,
            progress=progress,
            deadline=deadline
        )
        with new_session() as s:
            s.add(new_task)
            s.commit()
            return new_task

    @staticmethod
    def get_login(username, password):
        password = passwordHash.blake2b_hash(password)
        return session.query(Users).filter(Users.username == username, Users.password_hash == password).scalar()

    @staticmethod
    def delete_user(username):
        with new_session() as s:
            user_to_delete = s.execute(
                select(Users)
                .where(Users.username == username)  # type: ignore
            )
            if user_to_delete is None:
                return None
            s.delete(user_to_delete)
            s.commit()
            return True



    @staticmethod
    def number_of_all_users():
        all_user_count = session.query(Users).count()
        return all_user_count

    @staticmethod
    def get_all_users_tasks(username: str):
        with new_session() as t_session:
            user_id = DatabaseManager().get_user_id_by_username(username)

            users_tasks = t_session.execute(
                select(Tasks).where(Tasks.employee_id == user_id)  # type: ignore
            )

            return users_tasks.scalars().all()

    @staticmethod
    def add_comment(task_id: int, user_id: int, text: str, attached_file=None):
        with new_session() as s:
            user = s.execute(
                select(Users)
                .where(Users.id == user_id)
            ).scalar_one_or_none()
            if user is None:
                return None

            task = s.execute(
                select(Tasks)
                .where(Tasks.id == task_id)
            ).scalar_one_or_none()
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
            s.commit()
            return new_comment

    @staticmethod
    def add_comment2(user_id, text, task_id):
        with new_session() as s:
            user = s.execute(
                select(Users)
                .where(user_id == Users.id)  # type: ignore
            ).scalar_one_or_none()
            task = s.execute(
                select(Tasks)
                .where(task_id == Tasks.id)  # type: ignore
            ).scalar_one_or_none()
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
            s.commit()
            return new_comment

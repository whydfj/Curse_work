from fastapi import Depends
from sqlalchemy import select

from DB_SQLite.data_base_work import session, Users, Tasks, Comment, UserSettings, new_session
from Password_hash import passwordHash


class DatabaseManager:
    @staticmethod
    def get_all_users():
        return session.query(Users).all()

    @staticmethod
    def get_user_by_username(username):
        return session.query(Users).filter(Users.username == username).first()


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
        return session.query(Users).filter(Users.username == username).first().id

    @staticmethod
    def get_user_id_by_username2(username):
        with new_session() as s:
            return s.execute(
                select(Users.id).where(Users.username == username) # type: ignore
            ).scalar()

    @staticmethod
    def get_tasks_by_user(user_id):
        return session.query(Tasks).filter(Tasks.employee_id == user_id).all()

    @staticmethod
    def create_user(username, password_hash, role, name, surname):
        new_user = Users(
            username=username,
            password_hash=passwordHash.blake2b_hash(password_hash),
            role=role,
            name=name,
            surname=surname
        )
        session.add(new_user)
        session.commit()
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
        session.add(new_task)
        session.commit()
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
        session.add(new_task)
        session.commit()
        return new_task

    @staticmethod
    def get_login(username, password):
        password = passwordHash.blake2b_hash(password)
        return session.query(Users).filter(Users.username == username, Users.password_hash == password).scalar()

    @staticmethod
    def delete_user(username):
        user_to_delete = session.query(Users).filter(Users.username == username).first()
        if user_to_delete is None:
            return None
        session.delete(user_to_delete)
        session.commit()
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
                select(Tasks).where(Tasks.employee_id == user_id)
            )

            return users_tasks.scalars().all()


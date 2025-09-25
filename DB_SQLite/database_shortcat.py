from DB_SQLite.data_base_work import session, User, Task, Comment, UserSettings
from Password_hash import passwordHash


class DatabaseManager:
    @staticmethod
    def get_all_users():
        return session.query(User).all()

    @staticmethod
    def get_user_by_username(username):
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_tasks_by_user(user_id):
        return session.query(Task).filter(Task.employee_id == user_id).all()

    @staticmethod
    def create_user(username, password_hash, role, name, surname):
        new_user = User(
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
        new_task = Task(
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
    def get_login(username,password):
        password = passwordHash.blake2b_hash(password)
        return session.query(User).filter(User.username == username , User.password_hash == password).scalar()

#DatabaseManager.create_user("admin1","123","employee","Ivan","Vasin");

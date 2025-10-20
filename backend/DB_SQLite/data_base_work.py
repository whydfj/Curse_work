import asyncio

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, BLOB, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime, timedelta


#Подключение к бд
engine = create_async_engine("sqlite+aiosqlite:///Coursework.db")
Session = async_sessionmaker(bind=engine)
new_session = async_sessionmaker(bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60))
    password_hash = Column(String(256))
    role = Column(String(10))
    name = Column(String(45))
    surname = Column(String(45))
    created_at = Column(String, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    tasks = relationship("Tasks", back_populates="employee")
    comments = relationship("Comment", back_populates="user")
    settings = relationship("UserSettings", back_populates="user")

class Tasks(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('Users.id'))
    title = Column(String(100))
    description = Column(Text)
    deadline = Column(DateTime, default=lambda: (datetime.now() + timedelta(days=30)).replace(microsecond=0))
    status = Column(String(10))
    progress = Column(Integer)
    created_at = Column(String, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    employee = relationship("Users", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")


class Comment(Base):
    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('Tasks.id'))
    user_id = Column(Integer, ForeignKey('Users.id'))
    text = Column(Text)
    attached_file = Column(BLOB)
    created_at = Column(String, default=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    task = relationship("Tasks", back_populates="comments")
    user = relationship("Users", back_populates="comments")


class UserSettings(Base):
    __tablename__ = 'User_settings'

    employee_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    theme_style = Column(Integer)
    language_app = Column(String(15))
    avatar = Column(BLOB)

    user = relationship("Users", back_populates="settings")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Пример использования
async def main():
    # Инициализация БД
    await init_db()

# В конце файла добавьте:
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())





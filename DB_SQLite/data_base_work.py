from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#Подключение к бд
engine = create_engine("sqlite+pysqlite:///Coursework.db")

#with engine.connect() as connection:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#Подключение к бд
engine = create_engine("sqlite:///Coursework.db")

new_session = sessionmaker(bind=engine)
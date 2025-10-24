import sqlite3 as sq
import os


DB_PATH = os.path.join(os.path.dirname(__file__), "Coursework.db")


with sq.connect(DB_PATH) as con:
    cur = con.cursor()

    cur.execute('''drop table if exists Users;''')
    cur.execute('''
    create table Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username varchar(60) UNIQUE,
        password_hash VARCHAR(256),
        role TEXT CHECK(role IN ('manager', 'employee')) DEFAULT 'employee',
        name varchar(45),
        surname varchar(45),
        created_at TEXT default (datetime('now','+3 hour')),
        email_user varchar(60) UNIQUE
    )''')

    cur.execute('''drop table if exists Tasks;''')
    cur.execute('''
    create table Tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        employee_id INTEGER NOT NULL,
        title VARCHAR(100),
        description TEXT,
        deadline TEXT default (datetime('now','+3 hour','+30 day')),
        status TEXT CHECK(status IN ('running', 'completed','frozen')) DEFAULT 'running',
        progress INTEGER CHECK(progress >= 0 AND progress <= 100) DEFAULT 0,
        created_at TEXT default (datetime('now','+3 hour')),

        FOREIGN KEY (employee_id) REFERENCES Users(id)
    )''')

    cur.execute('''drop table if exists Comments;''')
    cur.execute('''
        create table Comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            `text` TEXT,
            attached_file BLOB,
            created_at TEXT default (datetime('now','+3 hour')),

            FOREIGN KEY (task_id) REFERENCES Tasks(id),
            FOREIGN KEY (user_id) REFERENCES Users(id)
    )''')

    cur.execute('''drop table if exists User_settings;''')
    cur.execute('''
    create table User_settings(
        employee_id INTEGER NOT NULL,
        theme_style INTEGER CHECK(theme_style >= 0 AND theme_style <= 1) DEFAULT 0,
        language_app TEXT CHECK(language_app IN ('russian', 'english','Belarusian')) DEFAULT 'russian',
        avatar BlOB,
        
        FOREIGN KEY (employee_id) REFERENCES Users(id)
    )''')

    cur.execute('''
        INSERT INTO Users(username,password_hash,role,name,surname,email_user)
        VALUES('admin','344b8a854221bd1eaf9382daaea1996fbcd496f158e983f8835c7ef5084c55bb','manager','Ivan','Ivanov','skorpy729@gmail.com')
    ''')#пароль для админа - password
    cur.execute('''
        INSERT INTO Users(username,password_hash,role,name,surname,email_user)
        VALUES('user','4361be62001d25deb2bd85fab3e46011afae57539026d8d37d57f45e29571271','employee','Aleksander','Shnaider','globalfetish666@gmail.com')
    ''')#пароль для user 123456

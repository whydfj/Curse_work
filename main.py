from fastapi import FastAPI


import sqlite3 as sq

with sq.connect("Coursework.db") as con:
    cur = con.cursor()  # выбираем эту БД

    cur.execute('''drop table if exists Users;''')
    cur.execute('''
    create table Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username varchar(60) UNIQUE,
        password_hash VARCHAR(256),
        role TEXT CHECK(role IN ('manager', 'employee')) DEFAULT 'employee',
        name varchar(45),
        surname varchar(45),
        created_at TEXT default (datetime('now'))
    )''')

    cur.execute('''drop table if exists Tasks;''')
    cur.execute('''
    create table Tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        employee_id INTEGER NOT NULL,
        title VARCHAR(100),
        description TEXT,
        deadline TEXT default (datetime('now','+30 day')),
        status TEXT CHECK(status IN ('running', 'completed','frozen')) DEFAULT 'running',
        progress INTEGER CHECK(progress >= 0 AND progress <= 100) DEFAULT 0,
        created_at TEXT default (datetime('now')),

        FOREIGN KEY (employee_id) REFERENCES Users(id)
    )''')

    cur.execute('''drop table if exists Comments;''')
    cur.execute('''
        create table Comments(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            task_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            `text` TEXT,
            created_at TEXT default (datetime('now')),

            FOREIGN KEY (task_id) REFERENCES Tasks(id),
            FOREIGN KEY (user_id) REFERENCES Users(id)
    )''')

    cur.execute('''
        INSERT INTO Users(username,password_hash,role,name,surname)
        VALUES('admin','password','manager','Ivan','Ivanov')
    ''')

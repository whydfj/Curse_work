import sqlite3 as sq

with sq.connect("../Coursework.db") as con:
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
        created_at TEXT default (datetime('now','+3 hour'))
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
        INSERT INTO Users(username,password_hash,role,name,surname)
        VALUES('admin','password','manager','Ivan','Ivanov')
    ''')
    cur.execute('''
        INSERT INTO Users(username,password_hash,role,name,surname)
        VALUES('user','123456','employee','Aleksander','Shnaider')
    ''')

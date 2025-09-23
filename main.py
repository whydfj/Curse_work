from fastapi import FastAPI#перешли на 3.12 теперь точно jfjfjfЛАЛЛАЛА


app = FastAPI()


@app.get("/")
def main_page():
    p = 0
    if p == 2:
        return {"qq": 1}

    return {"message": "Welcome to main page!"}



@app.get("/data")
def all_data():
    return {"message": "Типа вывелась вся бд"}




#k;wehbdcjedc popa pisya
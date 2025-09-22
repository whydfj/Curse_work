from fastapi import FastAPI


app = FastAPI()#фастапи gjgjgjg))


@app.get("/")
def main_page():
    return {"message": "Welcome to main page!"}


@app.get("/data")
def all_data():
    return {"message": "Типа вывелась вся бд"}
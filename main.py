from fastapi import FastAPI#перешли на 3.12 теперь точно


app = FastAPI()


@app.get("/")
def main_page():
    return {"message": "Welcome to main page!"}


@app.get("/data")
def all_data():
    return {"message": "Типа вывелась вся бд"}
from fastapi import FastAPI,HTTPException


app = FastAPI()


@app.get("/")
def main_page():
    p = 0
    if p == 2:
        return {"qq": 1}

    raise HTTPException(status_code=404,detail="не найдено(")



@app.get("/data")
def all_data():
    return {"message": "Типа вывелась вся бд"}

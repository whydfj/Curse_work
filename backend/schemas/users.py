from pydantic import BaseModel, Field


class User_Login_Schema(BaseModel):
    username: str = Field(max_length=60)
    password: str = Field(max_length=20)


class User_Create_Schema(BaseModel):
    username: str = Field(max_length=60)
    password: str = Field(max_length=20)
    role: str = Field(max_length=10)
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)


class User_Found_and_Delete_Schema(BaseModel):
    username: str = Field(max_length=60)


class Comment_Schema(BaseModel):
    task_id: int
    text: str
    attached_file: None

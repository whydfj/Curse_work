from typing import Optional

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
    email_user: str = Field(max_length=60)


class User_Found_and_Delete_Schema(BaseModel):
    username: str = Field(max_length=60)


class Comment_Schema(BaseModel):
    task_id: int
    text: str
    attached_file: None


class DeleteCommentSchema(BaseModel):
    comment_id: int


class Update_Settings_Schema(BaseModel):
    new_lang: Optional[str] = None
    new_theme: Optional[int] = None


class AI_Request_Schema(BaseModel):
    question: str


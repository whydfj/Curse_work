from datetime import datetime

from pydantic import BaseModel, Field


class Task_Schema(BaseModel):
    username: str
    title: str
    description: str
    deadline: datetime | None


class Task_Delete_Schema(BaseModel):
    username: str
    title: str


class Task_Set_Schema(BaseModel):
    username: str
    title: str
    new_title: str
    new_description: str


class Deadline_Set_Schema(BaseModel):
    task_id: int
    new_deadline: datetime


class Progress_Update_Schema(BaseModel):
    task_title: str
    progress: int = Field(ge=0, le=100)

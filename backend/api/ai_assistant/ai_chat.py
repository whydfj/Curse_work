from gigachat import GigaChat
from fastapi import APIRouter
from backend.schemas.users import AI_Request_Schema
from backend.api.ai_assistant.template import template


router = APIRouter()

giga = GigaChat(
    credentials="MDE5YTk3NGUtZDVmYS03ZmJiLWFkM2UtODk0Y2Q2MDQyNzU4OjZiZjZmYTdhLWI5MGQtNDhlYS05MWI3LTQ1MTM0MGEyZTEwNw==",
    verify_ssl_certs=False,
)


@router.post("/ai_request")
async def request_to_ai(user_request: AI_Request_Schema):
    response = giga.chat(template + user_request.question)

    return response.choices[0].message.content




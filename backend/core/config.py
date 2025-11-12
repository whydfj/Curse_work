import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent  # Поднимаемся до Curse_work/
env_path = BASE_DIR / '.env'

load_dotenv(env_path)

class EmailConfig:
    SMTP_SERVER = "smtp.yandex.ru"
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv("EMAIL_USER")
    SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

EMAIL_CONFIG = EmailConfig()


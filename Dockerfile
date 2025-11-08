FROM python:3.12.4

WORKDIR /app

# Копируем только requirements.txt для установки зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем весь код (а не только backend, если тебе нужны ещё файлы)
COPY . .

EXPOSE 8000
# Запускаем приложение через uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]


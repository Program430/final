FROM python:3.11-slim

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Запускаем приложение
CMD ["sh", "-c","alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
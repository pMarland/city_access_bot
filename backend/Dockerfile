FROM python:3.11-slim

WORKDIR /app

# 1. зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. копируем ВСЁ backend-содержимое
COPY . .

# 3. делаем entrypoint исполняемым (ЯВНЫЙ ПУТЬ)
RUN chmod +x /app/entrypoint.sh

# 4. entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# 5. команда запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

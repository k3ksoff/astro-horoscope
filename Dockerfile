FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Делаем скрипт исполняемым
RUN chmod +x /app/scripts/entrypoint.sh

# Запускаем сервер
CMD ["sh", "/app/scripts/entrypoint.sh"] 
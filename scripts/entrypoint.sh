#!/bin/bash

# Создаем миграции и применяем их
python manage.py makemigrations horoscope
python manage.py migrate

# Создаем статические файлы
python manage.py collectstatic --noinput

# Создаем суперпользователя
echo "Creating superuser..."
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-adminpassword}

python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created successfully!');
else:
    print('Superuser already exists.');
"

# Инициализируем crontab (если установлен)
if python -c "import django_crontab" &> /dev/null; then
    echo "Настройка crontab для ежедневной генерации гороскопов..."
    python manage.py crontab add
fi

# Запускаем Gunicorn
gunicorn horoscope_project.wsgi:application --bind 0.0.0.0:8000 
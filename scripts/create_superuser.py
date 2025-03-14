import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horoscope_project.settings')
django.setup()

User = get_user_model()

DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')

if not User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists():
    print(f'Creating superuser {DJANGO_SUPERUSER_USERNAME}...')
    User.objects.create_superuser(
        username=DJANGO_SUPERUSER_USERNAME,
        email=DJANGO_SUPERUSER_EMAIL,
        password=DJANGO_SUPERUSER_PASSWORD
    )
    print('Superuser created successfully!')
else:
    print(f'Superuser {DJANGO_SUPERUSER_USERNAME} already exists.') 
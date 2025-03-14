from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import ZodiacSign, HoroscopePrediction
from .services import get_or_generate_horoscope, get_all_zodiac_signs, initialize_zodiac_signs


# Словарь совместимости знаков зодиака
COMPATIBILITY_DICT = {
    'Овен': ['Лев', 'Стрелец', 'Весы'],
    'Телец': ['Дева', 'Козерог', 'Рак'],
    'Близнецы': ['Весы', 'Водолей', 'Лев'],
    'Рак': ['Скорпион', 'Рыбы', 'Телец'],
    'Лев': ['Овен', 'Стрелец', 'Близнецы'],
    'Дева': ['Телец', 'Козерог', 'Скорпион'],
    'Весы': ['Близнецы', 'Водолей', 'Овен'],
    'Скорпион': ['Рак', 'Рыбы', 'Дева'],
    'Стрелец': ['Овен', 'Лев', 'Водолей'],
    'Козерог': ['Телец', 'Дева', 'Рыбы'],
    'Водолей': ['Близнецы', 'Весы', 'Стрелец'],
    'Рыбы': ['Рак', 'Скорпион', 'Козерог']
}


# Инициализация знаков зодиака после миграции
@receiver(post_migrate)
def populate_zodiac_signs(sender, **kwargs):
    if sender.name == 'horoscope':
        initialize_zodiac_signs()


def index(request):
    """Главная страница со списком знаков зодиака"""
    signs = get_all_zodiac_signs()
    today = timezone.localdate()
    return render(request, 'horoscope/index.html', {'signs': signs, 'today': today})


def sign_detail(request, sign_id):
    """Страница с детальным гороскопом для выбранного знака"""
    sign = get_object_or_404(ZodiacSign, id=sign_id)
    horoscope = get_or_generate_horoscope(sign_id=sign_id)
    compatible_signs = COMPATIBILITY_DICT.get(sign.name, [])
    
    return render(request, 'horoscope/sign_detail.html', {
        'sign': sign, 
        'horoscope': horoscope,
        'compatible_signs': compatible_signs
    })


def sign_by_name(request, sign_name):
    """Страница с детальным гороскопом по имени знака"""
    try:
        sign = ZodiacSign.objects.get(name__iexact=sign_name)
        return redirect('sign_detail', sign_id=sign.id)
    except ZodiacSign.DoesNotExist:
        signs = get_all_zodiac_signs()
        today = timezone.localdate()
        return render(request, 'horoscope/index.html', {
            'signs': signs, 
            'today': today, 
            'error': f'Знак зодиака "{sign_name}" не найден.'
        })


@require_http_methods(["GET"])
def api_get_horoscope(request, sign_id):
    """API для получения гороскопа в формате JSON"""
    horoscope = get_or_generate_horoscope(sign_id=sign_id)
    if not horoscope:
        return JsonResponse({'error': 'Знак зодиака не найден'}, status=404)
    
    return JsonResponse({
        'sign': horoscope.sign.name,
        'date': horoscope.date.strftime('%Y-%m-%d'),
        'prediction': horoscope.prediction,
        'love': horoscope.love,
        'career': horoscope.career,
        'health': horoscope.health,
        'lucky_number': horoscope.lucky_number
    }) 
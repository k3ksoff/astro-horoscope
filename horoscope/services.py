import random
from datetime import date
from django.utils import timezone
from .models import ZodiacSign, HoroscopePrediction, Prediction


def get_random_prediction(category):
    """Получает случайное предсказание из базы данных по категории"""
    predictions = Prediction.objects.filter(category=category)
    if predictions.exists():
        return random.choice(predictions).text
    
    # Если в базе нет предсказаний, используем запасные варианты
    default_predictions = {
        'general': [
            "Сегодня день, полный возможностей. Будьте открыты новому.",
            "Звезды советуют быть внимательнее к деталям сегодня.",
            "Хороший день для начала новых проектов и планов.",
            "Сегодня стоит сосредоточиться на личном развитии.",
            "День принесет неожиданные, но приятные сюрпризы.",
        ],
        'love': [
            "В личной жизни вас ждет гармония и понимание.",
            "Хороший день для романтического свидания.",
            "Звезды советуют быть более открытыми в отношениях.",
            "Возможна неожиданная встреча, которая изменит вашу жизнь.",
            "Проявите больше внимания к партнеру сегодня.",
        ],
        'career': [
            "На работе вас ждет продуктивный день.",
            "Хорошее время для демонстрации ваших профессиональных качеств.",
            "Возможны новые деловые предложения.",
            "День благоприятен для решения рабочих задач и общения с коллегами.",
            "Сосредоточьтесь на приоритетных задачах сегодня.",
        ],
        'health': [
            "Обратите внимание на свое здоровье. Больше отдыхайте.",
            "Хороший день для начала новой программы упражнений.",
            "Звезды советуют сбалансировать работу и отдых.",
            "Старайтесь избегать стрессовых ситуаций сегодня.",
            "Уделите время физической активности и правильному питанию.",
        ]
    }
    
    return random.choice(default_predictions.get(category, default_predictions['general']))


def generate_lucky_number():
    """Генерирует случайное счастливое число от 1 до 100"""
    return random.randint(1, 100)


def get_or_generate_horoscope(sign_id=None, sign_name=None):
    """Получает или генерирует гороскоп на сегодня для указанного знака зодиака"""
    today = timezone.localdate()
    
    # Определяем знак зодиака
    if sign_id:
        try:
            sign = ZodiacSign.objects.get(id=sign_id)
        except ZodiacSign.DoesNotExist:
            return None
    elif sign_name:
        try:
            sign = ZodiacSign.objects.get(name__iexact=sign_name)
        except ZodiacSign.DoesNotExist:
            return None
    else:
        return None
    
    # Проверяем, есть ли уже гороскоп на сегодня
    try:
        horoscope = HoroscopePrediction.objects.get(sign=sign, date=today)
    except HoroscopePrediction.DoesNotExist:
        # Генерируем новый гороскоп
        horoscope = HoroscopePrediction(
            sign=sign,
            date=today,
            prediction=get_random_prediction('general'),
            love=get_random_prediction('love'),
            career=get_random_prediction('career'),
            health=get_random_prediction('health'),
            lucky_number=generate_lucky_number()
        )
        horoscope.save()
    
    return horoscope


def get_all_zodiac_signs():
    """Получает все знаки зодиака из базы данных"""
    return ZodiacSign.objects.all()


def initialize_zodiac_signs():
    """Инициализирует базу данных стандартными знаками зодиака, если их нет"""
    if ZodiacSign.objects.exists():
        return
    
    zodiac_signs = [
        {
            'name': 'Овен',
            'date_range': '21 марта - 19 апреля',
            'description': 'Овен - первый знак зодиака. Управляется Марсом. Символизирует лидерство, энергию и энтузиазм.'
        },
        {
            'name': 'Телец',
            'date_range': '20 апреля - 20 мая',
            'description': 'Телец - второй знак зодиака. Управляется Венерой. Символизирует стабильность, упорство и практичность.'
        },
        {
            'name': 'Близнецы',
            'date_range': '21 мая - 20 июня',
            'description': 'Близнецы - третий знак зодиака. Управляется Меркурием. Символизирует общительность, любопытство и адаптивность.'
        },
        {
            'name': 'Рак',
            'date_range': '21 июня - 22 июля',
            'description': 'Рак - четвертый знак зодиака. Управляется Луной. Символизирует эмоциональность, заботу и интуицию.'
        },
        {
            'name': 'Лев',
            'date_range': '23 июля - 22 августа',
            'description': 'Лев - пятый знак зодиака. Управляется Солнцем. Символизирует творчество, благородство и лидерство.'
        },
        {
            'name': 'Дева',
            'date_range': '23 августа - 22 сентября',
            'description': 'Дева - шестой знак зодиака. Управляется Меркурием. Символизирует аналитический ум, внимание к деталям и трудолюбие.'
        },
        {
            'name': 'Весы',
            'date_range': '23 сентября - 22 октября',
            'description': 'Весы - седьмой знак зодиака. Управляется Венерой. Символизирует гармонию, справедливость и дипломатию.'
        },
        {
            'name': 'Скорпион',
            'date_range': '23 октября - 21 ноября',
            'description': 'Скорпион - восьмой знак зодиака. Управляется Плутоном и Марсом. Символизирует страсть, решительность и глубину.'
        },
        {
            'name': 'Стрелец',
            'date_range': '22 ноября - 21 декабря',
            'description': 'Стрелец - девятый знак зодиака. Управляется Юпитером. Символизирует оптимизм, свободу и философию.'
        },
        {
            'name': 'Козерог',
            'date_range': '22 декабря - 19 января',
            'description': 'Козерог - десятый знак зодиака. Управляется Сатурном. Символизирует амбиции, дисциплину и ответственность.'
        },
        {
            'name': 'Водолей',
            'date_range': '20 января - 18 февраля',
            'description': 'Водолей - одиннадцатый знак зодиака. Управляется Ураном и Сатурном. Символизирует оригинальность, независимость и прогресс.'
        },
        {
            'name': 'Рыбы',
            'date_range': '19 февраля - 20 марта',
            'description': 'Рыбы - двенадцатый знак зодиака. Управляется Нептуном и Юпитером. Символизирует интуицию, творчество и духовность.'
        },
    ]
    
    for sign_data in zodiac_signs:
        ZodiacSign.objects.create(**sign_data)


def generate_horoscope_with_gigachat(sign):
    """Генерирует гороскоп для знака зодиака с использованием GigaChat API"""
    from .gigachat_client import GigaChatClient
    
    client = GigaChatClient()
    horoscope_data = client.generate_horoscope(sign.name)
    
    # Создаем или обновляем запись гороскопа
    today = timezone.localdate()
    
    horoscope, created = HoroscopePrediction.objects.update_or_create(
        sign=sign,
        date=today,
        defaults={
            'prediction': horoscope_data.get('prediction', ''),
            'love': horoscope_data.get('love', ''),
            'career': horoscope_data.get('career', ''),
            'health': horoscope_data.get('health', ''),
            'lucky_number': horoscope_data.get('lucky_number', generate_lucky_number())
        }
    )
    
    return horoscope


def generate_horoscopes_for_all_signs():
    """Генерирует гороскопы для всех знаков зодиака"""
    signs = get_all_zodiac_signs()
    results = []
    
    for sign in signs:
        try:
            horoscope = generate_horoscope_with_gigachat(sign)
            results.append({
                'sign': sign.name,
                'success': True,
                'id': horoscope.id
            })
        except Exception as e:
            results.append({
                'sign': sign.name,
                'success': False,
                'error': str(e)
            })
    
    return results 
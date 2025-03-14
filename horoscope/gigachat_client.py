import json
import logging
from django.conf import settings
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

logger = logging.getLogger(__name__)

class GigaChatClient:
    """
    Клиент для работы с API GigaChat от Сбера с использованием официальной библиотеки
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'GIGACHAT_API_KEY', '')
        if not self.api_key:
            logger.warning("GIGACHAT_API_KEY не настроен в settings.py")
        
        # Настройка API-ключа для работы с GigaChat
        self.credentials = {
            "credentials": self.api_key,
            "scope": "GIGACHAT_API_PERS",
            "verify_ssl_certs": False,
            "model": "GigaChat-2-Max"
        }
    
    def generate_horoscope(self, zodiac_sign):
        """
        Генерация гороскопа для указанного знака зодиака с помощью GigaChat
        
        Возвращает словарь с ключами:
        - prediction: общее предсказание на день
        - love: предсказание в сфере любви
        - career: предсказание в сфере карьеры
        - health: предсказание в сфере здоровья
        - lucky_number: счастливое число дня
        """
        try:
            # Создаем экземпляр GigaChat
            with GigaChat(**self.credentials) as giga:
                
                # Составляем системный промпт
                system_prompt = (
                    "Ты - профессиональный астролог. Тебе нужно создать ежедневный гороскоп для указанного знака зодиака. "
                    "Твоя задача - сгенерировать короткий, правдивый и интересный гороскоп. "
                    "Предсказание должно содержать общую информацию на день, а также отдельные предсказания для сфер любви, карьеры и здоровья. "
                    "Также нужно выбрать одно счастливое число от 1 до 100. "
                    "Формат ответа должен быть СТРОГО в виде JSON объекта со следующими полями: "
                    "prediction, love, career, health, lucky_number. "
                    "Пример ответа: {"
                    '"prediction": ""'
                    '"love": ""'
                    '"career": ""'
                    '"health": ""'
                    '"lucky_number": 42'
                    "}"
                    "Используй только русский язык. Не используй слишком сложные термины. "
                    "Каждое предсказание должно быть длиной 1-3 предложения. "
                    "Не указывай дату или знак зодиака в предсказании - только само предсказание."
                )
                
                user_prompt = f"Создай гороскоп на сегодня для знака зодиака {zodiac_sign}."
                
                # Составляем сообщения для запроса
                messages = [
                    Messages(role=MessagesRole.SYSTEM, content=system_prompt),
                    Messages(role=MessagesRole.USER, content=user_prompt)
                ]
                
                # Отправляем запрос к API
                payload = Chat(
                    messages=messages,
                    temperature=1.0,
                    top_p=0.95,
                    n=1,
                    stream=False,
                    max_tokens=1000,
                    repetition_penalty=1.0
                )
                
                # Получаем ответ
                response = giga.chat(payload)
                content = response.choices[0].message.content
                
                # Обрабатываем полученный ответ
                try:
                    # Вырезаем только JSON часть из ответа, если нужно
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        content = content.split('```')[1].split('```')[0].strip()
                    
                    # Преобразуем строку JSON в словарь Python
                    horoscope_data = json.loads(content)
                    
                    # Валидация ответа
                    required_fields = ['prediction', 'love', 'career', 'health', 'lucky_number']
                    for field in required_fields:
                        if field not in horoscope_data:
                            logger.warning(f"Отсутствует обязательное поле '{field}' в ответе GigaChat")
                            horoscope_data[field] = ""
                    
                    # Преобразование lucky_number в число
                    if isinstance(horoscope_data['lucky_number'], str) and horoscope_data['lucky_number'].isdigit():
                        horoscope_data['lucky_number'] = int(horoscope_data['lucky_number'])
                    elif not isinstance(horoscope_data['lucky_number'], int):
                        horoscope_data['lucky_number'] = 7  # Значение по умолчанию
                    
                    # Ограничиваем число от 1 до 100
                    horoscope_data['lucky_number'] = max(1, min(100, horoscope_data['lucky_number']))
                    
                    return horoscope_data
                
                except json.JSONDecodeError:
                    logger.error(f"Не удалось разобрать JSON из ответа GigaChat: {content}")
                    return self._generate_fallback_horoscope(zodiac_sign)
        
        except Exception as e:
            logger.error(f"Ошибка при работе с GigaChat: {str(e)}")
            return self._generate_fallback_horoscope(zodiac_sign)
    
    def _generate_fallback_horoscope(self, zodiac_sign):
        """Генерация резервного гороскопа при ошибке с API"""
        from .services import get_random_prediction, generate_lucky_number
        
        return {
            "prediction": get_random_prediction('general'),
            "love": get_random_prediction('love'),
            "career": get_random_prediction('career'),
            "health": get_random_prediction('health'),
            "lucky_number": generate_lucky_number()
        } 
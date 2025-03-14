import logging
from django.utils import timezone
from .services import generate_horoscopes_for_all_signs

logger = logging.getLogger(__name__)


def generate_daily_horoscopes():
    """
    Задача для ежедневной генерации гороскопов для всех знаков зодиака.
    Запускается каждый день в 00:01.
    """
    logger.info(f"Запущена задача генерации гороскопов на {timezone.localdate()}")
    
    try:
        results = generate_horoscopes_for_all_signs()
        
        success_count = sum(1 for result in results if result.get('success', False))
        logger.info(f"Успешно сгенерировано гороскопов: {success_count} из {len(results)}")
        
        # Логируем неудачные попытки
        for result in results:
            if not result.get('success', False):
                logger.error(f"Не удалось сгенерировать гороскоп для {result.get('sign')}: {result.get('error')}")
        
        return True
    except Exception as e:
        logger.error(f"Ошибка при ежедневной генерации гороскопов: {str(e)}")
        return False 
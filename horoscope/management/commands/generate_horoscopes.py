from django.core.management.base import BaseCommand
from django.utils import timezone
from horoscope.services import generate_horoscopes_for_all_signs, get_all_zodiac_signs, generate_horoscope_with_gigachat


class Command(BaseCommand):
    help = 'Генерирует гороскопы для всех знаков зодиака или для конкретного знака с использованием GigaChat'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sign',
            type=str,
            help='Имя знака зодиака для генерации гороскопа (опционально)',
        )

    def handle(self, *args, **options):
        sign_name = options.get('sign')
        
        if sign_name:
            # Генерируем гороскоп для одного знака
            sign = None
            for s in get_all_zodiac_signs():
                if s.name.lower() == sign_name.lower():
                    sign = s
                    break
            
            if sign:
                self.stdout.write(self.style.NOTICE(f'Генерация гороскопа для {sign.name}...'))
                try:
                    horoscope = generate_horoscope_with_gigachat(sign)
                    self.stdout.write(self.style.SUCCESS(f'Гороскоп для {sign.name} успешно сгенерирован!'))
                    self.stdout.write(f'Общее предсказание: {horoscope.prediction}')
                    self.stdout.write(f'Любовь: {horoscope.love}')
                    self.stdout.write(f'Карьера: {horoscope.career}')
                    self.stdout.write(f'Здоровье: {horoscope.health}')
                    self.stdout.write(f'Счастливое число: {horoscope.lucky_number}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Ошибка при генерации гороскопа: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'Знак зодиака "{sign_name}" не найден.'))
                self.stdout.write('Доступные знаки:')
                for s in get_all_zodiac_signs():
                    self.stdout.write(f' - {s.name}')
        else:
            # Генерируем гороскопы для всех знаков
            self.stdout.write(self.style.NOTICE(f'Генерация гороскопов на {timezone.localdate()}...'))
            
            results = generate_horoscopes_for_all_signs()
            
            success_count = sum(1 for result in results if result.get('success', False))
            self.stdout.write(self.style.SUCCESS(f'Успешно сгенерировано гороскопов: {success_count} из {len(results)}'))
            
            # Выводим информацию о неудачных попытках
            for result in results:
                if not result.get('success', False):
                    self.stdout.write(
                        self.style.ERROR(
                            f'Не удалось сгенерировать гороскоп для {result.get("sign")}: {result.get("error")}'
                        )
                    ) 
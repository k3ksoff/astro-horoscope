from django.db import models
from django.utils import timezone


class ZodiacSign(models.Model):
    """Модель для знаков зодиака"""
    name = models.CharField('Название', max_length=50)
    date_range = models.CharField('Период', max_length=100)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Знак зодиака'
        verbose_name_plural = 'Знаки зодиака'
        ordering = ['id']
    
    def __str__(self):
        return self.name


class HoroscopePrediction(models.Model):
    """Модель для предсказаний гороскопа"""
    sign = models.ForeignKey(ZodiacSign, on_delete=models.CASCADE, related_name='predictions', verbose_name='Знак зодиака')
    date = models.DateField('Дата', default=timezone.now)
    prediction = models.TextField('Предсказание')
    love = models.TextField('Любовь', blank=True)
    career = models.TextField('Карьера', blank=True)
    health = models.TextField('Здоровье', blank=True)
    lucky_number = models.IntegerField('Счастливое число', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Предсказание'
        verbose_name_plural = 'Предсказания'
        ordering = ['-date']
        unique_together = ['sign', 'date']  # Одно предсказание на знак в день
    
    def __str__(self):
        return f"{self.sign.name} - {self.date}"


class Prediction(models.Model):
    """Модель для шаблонов предсказаний"""
    category = models.CharField('Категория', max_length=50, choices=[
        ('general', 'Общее'),
        ('love', 'Любовь'),
        ('career', 'Карьера'),
        ('health', 'Здоровье'),
    ])
    text = models.TextField('Текст')
    
    class Meta:
        verbose_name = 'Шаблон предсказания'
        verbose_name_plural = 'Шаблоны предсказаний'
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.text[:50]}..." 
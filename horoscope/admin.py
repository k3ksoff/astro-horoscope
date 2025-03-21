from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import format_html
from django.contrib import messages
from django.template.response import TemplateResponse
from django.utils import timezone
from django.db.models import Count, Avg, F
from django.template.loader import render_to_string
from django.db.models.functions import Length
import csv
import datetime
import json
import re
from .models import ZodiacSign, HoroscopePrediction, Prediction
from .services import generate_horoscope_with_gigachat


@admin.register(ZodiacSign)
class ZodiacSignAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_range')
    search_fields = ('name',)


@admin.register(HoroscopePrediction)
class HoroscopePredictionAdmin(admin.ModelAdmin):
    list_display = ('sign', 'date', 'created_at', 'prediction_preview', 'actions_buttons')
    list_filter = ('sign', 'date')
    search_fields = ('sign__name', 'prediction')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)
    
    def prediction_preview(self, obj):
        return obj.prediction[:100] + '...' if len(obj.prediction) > 100 else obj.prediction
    
    prediction_preview.short_description = 'Предсказание'
    
    def actions_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}">Сгенерировать с GigaChat</a>',
            f"/admin/horoscope/horoscopeprediction/{obj.id}/generate-with-gigachat/"
        )
    
    actions_buttons.short_description = 'Действия'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:obj_id>/generate-with-gigachat/',
                self.admin_site.admin_view(self.regenerate_with_gigachat),
                name='horoscope_prediction_regenerate_with_gigachat',
            ),
            path(
                'generate-with-gigachat/',
                self.admin_site.admin_view(self.generate_with_gigachat_form),
                name='horoscope_prediction_generate_with_gigachat_form',
            ),
            path(
                'generate-with-gigachat/submit/',
                self.admin_site.admin_view(self.generate_with_gigachat_submit),
                name='horoscope_prediction_generate_with_gigachat_submit',
            ),
            path(
                'reports/',
                self.admin_site.admin_view(self.reports_view),
                name='horoscope_reports',
            ),
            path(
                'reports/generate/',
                self.admin_site.admin_view(self.generate_report),
                name='horoscope_generate_report',
            ),
            path(
                'reports/export-csv/',
                self.admin_site.admin_view(self.export_report_csv),
                name='horoscope_export_report_csv',
            ),
        ]
        return custom_urls + urls
    
    def regenerate_with_gigachat(self, request, obj_id):
        prediction = self.get_object(request, obj_id)
        try:
            generate_horoscope_with_gigachat(prediction.sign)
            self.message_user(
                request,
                f"Гороскоп для {prediction.sign.name} успешно обновлен с использованием GigaChat",
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(
                request,
                f"Ошибка при генерации гороскопа: {str(e)}",
                messages.ERROR
            )
        
        return HttpResponseRedirect("../")
    
    def generate_with_gigachat_form(self, request):
        # Отображение формы выбора знака зодиака
        signs = ZodiacSign.objects.all()
        context = {
            'title': 'Генерация гороскопа с использованием GigaChat',
            'signs': signs,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
        }
        return TemplateResponse(request, 'admin/horoscope/generate_with_gigachat_form.html', context)
    
    def generate_with_gigachat_submit(self, request):
        if request.method == 'POST':
            sign_id = request.POST.get('sign_id')
            try:
                sign = ZodiacSign.objects.get(id=sign_id)
                generate_horoscope_with_gigachat(sign)
                self.message_user(
                    request,
                    f"Гороскоп для {sign.name} успешно создан с использованием GigaChat",
                    messages.SUCCESS
                )
            except ZodiacSign.DoesNotExist:
                self.message_user(
                    request,
                    "Знак зодиака не найден",
                    messages.ERROR
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Ошибка при генерации гороскопа: {str(e)}",
                    messages.ERROR
                )
        
        return HttpResponseRedirect("../../")
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['generate_button'] = True
        extra_context['show_reports_button'] = True
        return super().changelist_view(request, extra_context=extra_context)
    
    def analyze_sentiment(self, text):
        """Простой анализ тональности текста"""
        positive_words = [
            'удача', 'успех', 'радость', 'счастье', 'позитив', 'любовь', 'благополучие', 
            'рост', 'улучшение', 'возможность', 'приятный', 'хороший', 'отличный', 
            'прекрасный', 'замечательный', 'везение', 'великолепный', 'благоприятный'
        ]
        negative_words = [
            'провал', 'неудача', 'проблема', 'сложность', 'трудность', 'печаль', 'грусть', 
            'упадок', 'конфликт', 'ухудшение', 'неприятный', 'плохой', 'тяжелый', 
            'депрессия', 'разочарование', 'напряжение', 'противоречие', 'плохо'
        ]
        
        text = text.lower()
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count > negative_count:
            return 'позитивный'
        elif negative_count > positive_count:
            return 'негативный'
        else:
            return 'нейтральный'
    
    def get_prediction_length(self, prediction):
        """Получить длину предсказания в словах"""
        if not prediction:
            return 0
        return len(re.findall(r'\b\w+\b', prediction))
        
    def reports_view(self, request):
        """Отображение страницы с выбором типа отчета"""
        signs = ZodiacSign.objects.all()
        today = timezone.now().date()
        month_ago = today - datetime.timedelta(days=30)
        
        context = {
            'title': 'Отчеты по гороскопам',
            'signs': signs,
            'opts': self.model._meta,
            'app_label': self.model._meta.app_label,
            'today': today.strftime('%Y-%m-%d'),
            'month_ago': month_ago.strftime('%Y-%m-%d'),
        }
        return TemplateResponse(request, 'admin/horoscope/horoscopeprediction/reports.html', context)
    
    def generate_report(self, request):
        """Генерация отчета на основе выбранных параметров"""
        if request.method == 'POST':
            report_type = request.POST.get('report_type')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            sign_id = request.POST.get('sign_id')
            
            # Базовый запрос для всех отчетов
            queryset = HoroscopePrediction.objects.all()
            
            # Применение фильтров
            if start_date:
                queryset = queryset.filter(date__gte=start_date)
            if end_date:
                queryset = queryset.filter(date__lte=end_date)
            if sign_id and sign_id != 'all':
                queryset = queryset.filter(sign_id=sign_id)
            
            context = {
                'title': 'Результаты отчета',
                'opts': self.model._meta,
                'app_label': self.model._meta.app_label,
                'report_type': report_type,
                'start_date': start_date,
                'end_date': end_date,
            }
            
            if report_type == 'predictions_by_sign':
                # Количество предсказаний по знакам зодиака
                report_data = list(queryset.values('sign__name').annotate(count=Count('id')).order_by('sign__name'))
                context['report_data'] = report_data
                context['report_title'] = 'Количество предсказаний по знакам зодиака'
                context['chart_labels'] = json.dumps([item['sign__name'] for item in report_data])
                context['chart_data'] = json.dumps([item['count'] for item in report_data])
            
            elif report_type == 'predictions_by_date':
                # Количество предсказаний по датам
                report_data = list(queryset.values('date').annotate(count=Count('id')).order_by('date'))
                context['report_data'] = report_data
                context['report_title'] = 'Количество предсказаний по датам'
                context['chart_labels'] = json.dumps([item['date'].strftime('%Y-%m-%d') for item in report_data])
                context['chart_data'] = json.dumps([item['count'] for item in report_data])
            
            elif report_type == 'lucky_numbers':
                # Статистика счастливых чисел
                report_data = list(queryset.exclude(lucky_number__isnull=True)
                                  .values('lucky_number')
                                  .annotate(count=Count('id'))
                                  .order_by('lucky_number'))
                context['report_data'] = report_data
                context['report_title'] = 'Статистика счастливых чисел'
                context['chart_labels'] = json.dumps([str(item['lucky_number']) for item in report_data])
                context['chart_data'] = json.dumps([item['count'] for item in report_data])
                
            elif report_type == 'sentiment_analysis':
                # Анализ тональности предсказаний
                predictions = list(queryset.select_related('sign'))
                sentiments = {
                    'позитивный': 0,
                    'нейтральный': 0,
                    'негативный': 0
                }
                
                report_data = []
                for prediction in predictions:
                    sentiment = self.analyze_sentiment(prediction.prediction)
                    sentiments[sentiment] += 1
                    report_data.append({
                        'sign': prediction.sign.name,
                        'date': prediction.date,
                        'sentiment': sentiment,
                        'words_count': self.get_prediction_length(prediction.prediction)
                    })
                
                sentiment_stats = [
                    {'sentiment': key, 'count': value} 
                    for key, value in sentiments.items()
                ]
                
                context['report_data'] = report_data
                context['sentiment_stats'] = sentiment_stats
                context['report_title'] = 'Анализ тональности предсказаний'
                context['chart_labels'] = json.dumps(list(sentiments.keys()))
                context['chart_data'] = json.dumps(list(sentiments.values()))
                
            elif report_type == 'detailed_predictions':
                # Детальный отчет по предсказаниям
                report_data = queryset.select_related('sign').order_by('-date', 'sign__name')
                context['report_data'] = report_data
                context['report_title'] = 'Детальный отчет по предсказаниям'
                
            # Сохраняем данные для возможного экспорта в CSV
            request.session['report_data'] = {
                'type': report_type,
                'params': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'sign_id': sign_id
                }
            }
            
            return TemplateResponse(request, 'admin/horoscope/horoscopeprediction/report_results.html', context)
        
        return HttpResponseRedirect("../reports/")
    
    def export_report_csv(self, request):
        """Экспорт отчета в формате CSV"""
        report_data = request.session.get('report_data', {})
        report_type = report_data.get('type')
        params = report_data.get('params', {})
        
        if not report_type:
            return HttpResponseRedirect("../reports/")
        
        # Формируем имя файла
        filename = f"horoscope_report_{report_type}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Создаем HTTP-ответ с правильным content-type и кодировкой
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Записываем BOM (Byte Order Mark) для корректного отображения в Excel
        response.write('\ufeff')
        
        # Создаем объект для записи CSV с разделителем точка с запятой
        writer = csv.writer(response, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Базовый запрос
        queryset = HoroscopePrediction.objects.all()
        
        # Применение фильтров
        if params.get('start_date'):
            queryset = queryset.filter(date__gte=params['start_date'])
        if params.get('end_date'):
            queryset = queryset.filter(date__lte=params['end_date'])
        if params.get('sign_id') and params['sign_id'] != 'all':
            queryset = queryset.filter(sign_id=params['sign_id'])
        
        if report_type == 'predictions_by_sign':
            writer.writerow(['Знак зодиака', 'Количество предсказаний'])
            report_data = queryset.values('sign__name').annotate(count=Count('id')).order_by('sign__name')
            for item in report_data:
                writer.writerow([item['sign__name'], item['count']])
                
        elif report_type == 'predictions_by_date':
            writer.writerow(['Дата', 'Количество предсказаний'])
            report_data = queryset.values('date').annotate(count=Count('id')).order_by('date')
            for item in report_data:
                writer.writerow([item['date'].strftime('%d.%m.%Y'), item['count']])
                
        elif report_type == 'lucky_numbers':
            writer.writerow(['Счастливое число', 'Количество предсказаний'])
            report_data = queryset.exclude(lucky_number__isnull=True).values('lucky_number').annotate(count=Count('id')).order_by('lucky_number')
            for item in report_data:
                writer.writerow([item['lucky_number'], item['count']])
                
        elif report_type == 'sentiment_analysis':
            writer.writerow(['Знак зодиака', 'Дата', 'Тональность', 'Количество слов'])
            predictions = queryset.select_related('sign')
            for prediction in predictions:
                sentiment = self.analyze_sentiment(prediction.prediction)
                words_count = self.get_prediction_length(prediction.prediction)
                writer.writerow([
                    prediction.sign.name,
                    prediction.date.strftime('%d.%m.%Y'),
                    sentiment,
                    words_count
                ])
                
        elif report_type == 'detailed_predictions':
            writer.writerow(['Дата', 'Знак зодиака', 'Предсказание', 'Любовь', 'Карьера', 'Здоровье', 'Счастливое число'])
            report_data = queryset.select_related('sign').order_by('-date', 'sign__name')
            for item in report_data:
                writer.writerow([
                    item.date.strftime('%d.%m.%Y'),
                    item.sign.name,
                    item.prediction,
                    item.love,
                    item.career,
                    item.health,
                    item.lucky_number or ''
                ])
        
        return response


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('category', 'text_preview')
    list_filter = ('category',)
    search_fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    
    text_preview.short_description = 'Текст' 
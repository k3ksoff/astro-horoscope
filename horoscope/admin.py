from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib import messages
from django.template.response import TemplateResponse
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
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('category', 'text_preview')
    list_filter = ('category',)
    search_fields = ('text',)
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    
    text_preview.short_description = 'Текст' 
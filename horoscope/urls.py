from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign/<int:sign_id>/', views.sign_detail, name='sign_detail'),
    path('sign/<str:sign_name>/', views.sign_by_name, name='sign_by_name'),
    path('api/horoscope/<int:sign_id>/', views.api_get_horoscope, name='api_get_horoscope'),
] 
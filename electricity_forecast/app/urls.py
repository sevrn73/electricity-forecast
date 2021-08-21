from django.urls import path
from app.views import index


urlpatterns = [
    # Основные представления
    path('', index, name='index'),  # Главная
]

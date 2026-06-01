from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница вызывает функцию index из views.py
]
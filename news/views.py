from django.shortcuts import render
from .models import New

def news_list(request):
    """Отображение страницы со списком новостей"""
    news = New.objects.all().order_by('-created_at')  # Сортируем по полю created_at
    return render(request, 'news.html', {'news': news})

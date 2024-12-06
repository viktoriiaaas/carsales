from django.shortcuts import render
from .models import New
from django.db.models import Q
from django.http import JsonResponse
from .serializers import NewSerializer

def news_list(request):
    """Отображение страницы со списком новостей"""
    news = New.objects.all().order_by('-created_at')  # Сортируем по полю created_at
    return render(request, 'news.html', {'news': news})

def filtered_news(request):
    """Фильтрация новостей с использованием Q объектов"""
    news_items = New.objects.filter(
        (Q(category__name='Новости') & Q(title__icontains='автомобиль')) |  # Категория новости и заголовок содержит "автомобиль" (AND)
        Q(content__icontains='новинка') &                                   # Или контент содержит слово "новинка" (OR)
        ~Q(profile__username='admin')                                       # Не создано профилем admin (NOT)
    )
    serializer = NewSerializer(news_items, many=True)
    return JsonResponse(serializer.data, safe=False)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import New
from .serializers import NewSerializer

def news_list(request):
    """Отображение страницы со списком новостей"""
    news = New.objects.all().order_by('-created_at')  # Сортируем по полю created_at
    return render(request, 'news.html', {'news': news})


class FilteredNewsAPIView(APIView):
    """Фильтрация новостей с использованием Q-запросов и APIView."""

    def get(self, request):
        category = request.GET.get('category')  # Фильтр по категории
        title_keyword = request.GET.get('title_keyword')  # Фильтр по ключевым словам в заголовке
        content_keyword = request.GET.get('content_keyword')  # Фильтр по ключевым словам в контенте
        exclude_user = request.GET.get('exclude_user')  # Исключить новости, созданные определенным пользователем

        # Создаем фильтры
        filters = Q()
        if category:
            filters &= Q(category__name__iexact=category)
        if title_keyword:
            filters &= Q(title__icontains=title_keyword)
        if content_keyword:
            filters |= Q(content__icontains=content_keyword)  # OR условие для контента
        if exclude_user:
            filters &= ~Q(profile__username=exclude_user)  # NOT условие для исключения пользователя

        # Фильтруем новости
        news_items = New.objects.filter(filters)
        if not news_items.exists():
            return Response({"error": "No news match the given filters"}, status=status.HTTP_404_NOT_FOUND)

        # Сериализуем и возвращаем данные
        serializer = NewSerializer(news_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
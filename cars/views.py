from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from cars.models import Auto, AutoPhoto
from django.db.models import Q
import json
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import AutoSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

def index(request):
    """Главная страница с выводом автомобилей и их фотографий"""
    autos = Auto.objects.all()[:10]  # Показываем первые 10 автомобилей
    autos_with_photos = []

    for auto in autos:
        # Получаем связанные фотографии для каждого автомобиля
        photos = AutoPhoto.objects.filter(auto=auto).select_related('photo')
        photo_urls = [ap.photo.url for ap in photos]  # Извлекаем только URL фотографий
        autos_with_photos.append({'auto': auto, 'photo_urls': photo_urls})

    return render(request, 'index.html', {'autos_with_photos': autos_with_photos})

# API для списка автомобилей с фильтрацией по статусу продажи
class AutoListView(generics.ListAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [SearchFilter]  # Добавляем SearchFilter
    search_fields = ['brand__name', 'model', 'description']  # Указываем поля, по которым будет выполняться поиск
    serializer_class = AutoSerializer

    def get_queryset(self):
        sell_status = self.request.GET.get('sell_status')
        if sell_status:
            return Auto.objects.filter(sell_status=sell_status)
        return Auto.objects.all()

# Детальная информация об автомобиле
def auto_detail(request, pk):
    if request.method == "GET":
        auto = get_object_or_404(Auto, pk=pk)
        serializer = AutoSerializer(auto)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])

# Создание нового автомобиля
def auto_create(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Получаем данные из тела запроса
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON data")
        serializer = AutoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

# Удаление автомобиля
def auto_delete(request, pk):
    if request.method == "DELETE":
        auto = get_object_or_404(Auto, pk=pk)
        auto.delete()
        return JsonResponse({'message': 'Auto deleted'}, status=204)
    else:
        return HttpResponseNotAllowed(['DELETE'])

# Фильтрация автомобилей с использованием Q объектов
def filtered_autos(request):
    autos = Auto.objects.filter(
        (Q(brand__name='BMW') | Q(year__gt=2015)) &  
        Q(mileage__lt=100000) &                      
        ~Q(sell_status__name='Продан')               
    )
    serializer = AutoSerializer(autos, many=True)
    return JsonResponse(serializer.data, safe=False)

# Фильтрация по году выпуска через GET-параметр year
def filter_autos_by_year(request):
    year = request.GET.get('year')
    if year:
        autos = Auto.objects.filter(year=year)
    else:
        autos = Auto.objects.all()
    serializer = AutoSerializer(autos, many=True)
    return JsonResponse(serializer.data, safe=False)

# Фильтрация по региону (именованные аргументы в URL)
def filter_autos_by_region(request, region_id):
    autos = Auto.objects.filter(region__id=region_id)
    serializer = AutoSerializer(autos, many=True)
    return JsonResponse(serializer.data, safe=False)

# Фильтрация по диапазону годов выпуска
def filter_autos_by_year_range(request):
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    autos = Auto.objects.all()
    if year_min:
        autos = autos.filter(year__gte=year_min)
    if year_max:
        autos = autos.filter(year__lte=year_max)
    serializer = AutoSerializer(autos, many=True)
    return JsonResponse(serializer.data, safe=False)

# Фильтрация по текущему аутентифицированному пользователю
class UserAutosListView(generics.ListAPIView):
    serializer_class = AutoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Auto.objects.filter(profile=self.request.user)

# Фильтрация по цвету автомобиля через GET-параметр color
def filter_autos_by_color(request):
    color = request.GET.get('color')
    if color:
        autos = Auto.objects.filter(color__name__iexact=color)
    else:
        autos = Auto.objects.all()
    serializer = AutoSerializer(autos, many=True)
    return JsonResponse(serializer.data, safe=False)


class AutoViewSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer

    @action(methods=['get'], detail=False, url_path='in-stock-autos')
    def in_stock_autos(self, request):
        """Метод для получения списка автомобилей в наличии"""
        in_stock_autos = Auto.objects.filter(sell_status__name='В наличии')
        serializer = self.get_serializer(in_stock_autos, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='update-price')
    def update_price(self, request, pk=None):
        """Метод для обновления цены конкретного автомобиля"""
        auto = self.get_object()
        new_price = request.data.get('price')

        if not new_price:
            return Response({'error': 'Цена не указана'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            auto.price = float(new_price)
            auto.save()
            return Response({'message': 'Цена успешно обновлена', 'new_price': auto.price}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Некорректная цена'}, status=status.HTTP_400_BAD_REQUEST)
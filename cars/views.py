from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from cars.models import Auto, AutoPhoto
from django.db.models import Q
import json
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import AutoSerializer


def filter_cars(request):
    """
    Фильтрация автомобилей с использованием Q-запросов (OR, AND, NOT).
    """
    print("Filter cars function accessed")
    print("Request parameters:", request.GET)

    # Получаем параметры из запроса
    brand = request.GET.get('brand')  # Параметр "Марка автомобиля"
    year_min = request.GET.get('year_min')  # Минимальный год выпуска
    year_max = request.GET.get('year_max')  # Максимальный год выпуска
    exclude_status = request.GET.get('exclude_status')  # Исключить статус продажи
    mileage_max = request.GET.get('mileage_max')  # Максимальный пробег

    # Формируем фильтр с использованием OR, AND и NOT
    filters = Q()
    if brand:
        filters |= Q(brand__name__iexact=brand)  # OR: автомобили указанной марки
    if year_min:
        filters &= Q(year__gte=int(year_min))  # AND: год >= year_min
    if year_max:
        filters &= Q(year__lte=int(year_max))  # AND: год <= year_max
    if exclude_status:
        filters &= ~Q(sell_status__name__iexact=exclude_status)  # NOT: исключить статус
    if mileage_max:
        filters &= Q(mileage__lte=int(mileage_max))  # AND: пробег <= mileage_max

    cars = Auto.objects.filter(filters)
    if not cars.exists():
        return JsonResponse({"error": "No cars match the given filters"}, status=404)

    serializer = AutoSerializer(cars, many=True)
    return JsonResponse(serializer.data, safe=False)


def index(request):
    """Главная страница с выводом автомобилей и их фотографий"""
    autos = Auto.objects.all()[:10]  # Показываем первые 10 автомобилей
    autos_with_photos = []

    for auto in autos:
        # Получаем связанные фотографии через AutoPhoto
        photos = AutoPhoto.objects.filter(auto=auto).select_related('photo')
        autos_with_photos.append({'auto': auto, 'photos': photos})

    return render(request, 'index.html', {'autos_with_photos': autos_with_photos})


def auto_detail(request, pk):
    if request.method == "GET":
        auto = get_object_or_404(Auto, pk=pk)
        serializer = AutoSerializer(auto)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])


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


def auto_delete(request, pk):
    if request.method == "DELETE":
        auto = get_object_or_404(Auto, pk=pk)
        auto.delete()
        return JsonResponse({'message': 'Auto deleted'}, status=204)
    else:
        return HttpResponseNotAllowed(['DELETE'])


class AutoListView(generics.ListAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['brand__name', 'model', 'description']

    def get_queryset(self):
        sell_status = self.request.GET.get('sell_status')
        if sell_status:
            return Auto.objects.filter(sell_status=sell_status)
        return Auto.objects.all()


class AutoViewSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer

    @action(methods=['get'], detail=False, url_path='in-stock-autos')
    def in_stock_autos(self, request):
        in_stock_autos = Auto.objects.filter(sell_status__name='В наличии')
        serializer = self.get_serializer(in_stock_autos, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='update-price')
    def update_price(self, request, pk=None):
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

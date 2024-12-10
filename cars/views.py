from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from cars.models import Auto, AutoPhoto
from django.db.models import Q
import json
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from .serializers import AutoSerializer


def index(request):
    """Главная страница с выводом автомобилей и их фотографий"""
    autos = Auto.objects.all()[:10]
    autos_with_photos = [
        {"auto": auto, "photos": AutoPhoto.objects.filter(auto=auto)}
        for auto in autos
    ]
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

    @action(methods=['GET'], detail=False, url_path='recommended-autos')
    def recommended_autos(self, request):
        """
        Рекомендованные автомобили:
        - Марки BMW или Mercedes
        - Цена менее 5,000,000
        - Год выпуска начиная с 2015
        """
        recommended_cars = Auto.objects.filter(
            (Q(brand__name__icontains="BMW") | Q(brand__name__icontains="Mercedes-Benz")) &  # OR
            ~Q(price__gte=5000000) &  # NOT
            Q(year__gte=2015)  # AND
        )
        if not recommended_cars.exists():
            return Response({"message": "No recommended cars found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(recommended_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='luxury-autos')
    def luxury_autos(self, request):
        """
        Премиальные автомобили:
        - Марки Porsche или Lexus
        - Пробег менее 100,000
        - Доступны только в регионе "Москва"
        """
        luxury_cars = Auto.objects.filter(
            (Q(brand__name__icontains="Porsche") | Q(brand__name__icontains="Lexus")) &  # OR
            ~Q(mileage__gte=100000) &  # NOT
            Q(region__name__icontains="Москва")  # AND
        )
        if not luxury_cars.exists():
            return Response({"message": "No luxury cars found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(luxury_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

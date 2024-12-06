from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from cars.models import Auto
from .serializers import AutoSerializer
import json


def index(request):
    """Главная страница с выводом автомобилей"""
    autos = Auto.objects.all()[:10]  # Показываем первые 10 автомобилей
    return render(request, 'index.html', {'autos': autos})


def auto_list(request):
    """Список всех автомобилей"""
    if request.method == "GET":
        autos = Auto.objects.all()
        serializer = AutoSerializer(autos, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])


def auto_detail(request, pk):
    """Детальная информация об автомобиле"""
    if request.method == "GET":
        auto = get_object_or_404(Auto, pk=pk)
        serializer = AutoSerializer(auto)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseNotAllowed(['GET'])


def auto_create(request):
    """Создание нового автомобиля"""
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
    """Удаление автомобиля"""
    if request.method == "DELETE":
        auto = get_object_or_404(Auto, pk=pk)
        auto.delete()
        return JsonResponse({'message': 'Auto deleted'}, status=204)
    else:
        return HttpResponseNotAllowed(['DELETE'])

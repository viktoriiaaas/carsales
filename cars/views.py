from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from cars.models import Auto, AutoPhoto
from django.db.models import Q
import json
from cars.models import Auto, Brand, BodyType, EngineType, Color, Region, SellStatus, Profile
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from .serializers import AutoSerializer
from rest_framework import viewsets, status
from .serializers import AutoSerializer, BrandSerializer, ProfileSerializer

class AutoFilterAPIView(generics.ListAPIView):
    """
    API для фильтрации автомобилей.
    """
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['brand__name', 'model', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        region = self.request.GET.get('region')
        year = self.request.GET.get('year')

        if brand:
            queryset = queryset.filter(brand__name__icontains=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if region:
            queryset = queryset.filter(region__name__icontains=region)
        if year:
            queryset = queryset.filter(year=year)

        return queryset

def index(request):

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
  
class BrandViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с марками автомобилей.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с профилями пользователей.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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
            (Q(brand__name__icontains="BMW") | Q(brand__name__icontains="Mercedes-Benz")) &  # или
            ~Q(price__gte=5000000) &  # не
            Q(year__gte=2015)  # и
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
    
    @action(methods=['POST'], detail=False, url_path='create-auto')
    def create_auto(self, request):
        """
        Метод для создания нового автомобиля через POST-запрос.
        """
        # Получение данных из тела запроса
        data = request.data

        try:
            # Проверка пользователя
            user = request.user
            if not user.is_authenticated:
                return Response({"error": "Вы должны быть авторизованы, чтобы создать автомобиль"}, status=status.HTTP_401_UNAUTHORIZED)

            # Проверка связанного профиля
            try:
                profile = Profile.objects.get(id=user.id)
            except Profile.DoesNotExist:
                return Response({"error": "У текущего пользователя нет связанного профиля"}, status=status.HTTP_400_BAD_REQUEST)

            # Получение связанных моделей
            brand = Brand.objects.get(id=data.get("brand_id"))
            body_type = BodyType.objects.get(id=data.get("body_type_id"))
            engine_type = EngineType.objects.get(id=data.get("engine_type_id"))
            color = Color.objects.get(id=data.get("color_id"))
            region = Region.objects.get(id=data.get("region_id"))
            sell_status = SellStatus.objects.get(id=data.get("sell_status_id"))

            # Создание автомобиля
            auto = Auto.objects.create(
                brand=brand,
                model=data.get("model"),
                year=data.get("year"),
                description=data.get("description", ""),
                mileage=data.get("mileage"),
                price=data.get("price"),
                body_type=body_type,
                engine_type=engine_type,
                color=color,
                region=region,
                sell_status=sell_status,
                profile=profile
            )

            serializer = AutoSerializer(auto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Brand.DoesNotExist:
            return Response({"error": "Указанная марка не найдена"}, status=status.HTTP_400_BAD_REQUEST)
        except BodyType.DoesNotExist:
            return Response({"error": "Указанный тип кузова не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except EngineType.DoesNotExist:
            return Response({"error": "Указанный тип двигателя не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Color.DoesNotExist:
            return Response({"error": "Указанный цвет не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Region.DoesNotExist:
            return Response({"error": "Указанный регион не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except SellStatus.DoesNotExist:
            return Response({"error": "Указанный статус продажи не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return Response({"error": f"Отсутствует поле: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Ошибка сервера: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# поиск по содержанию
class AutoSearchAPIView(ListAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['brand__name', 'model', 'description']
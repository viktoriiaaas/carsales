from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars.views import (
    AutoListView, AutoViewSet,  AutoFilterAPIView, AutoSearchAPIView, BrandViewSet, ProfileViewSet, index, auto_create, auto_delete, auto_detail
)

from news import views as news_views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'autos', AutoViewSet, basename='autos')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    # Главная страница
    path('', index, name='index'),

    # Админка
    path('admin/', admin.site.urls),


    # Маршруты для приложения cars

    path('api/autos/', AutoListView.as_view(), name='auto-list'),
    path('api/autos/filter/', AutoFilterAPIView.as_view(), name='auto-filter'),

    path('api/autos/search/', AutoSearchAPIView.as_view(), name='auto-search'),

    path('api/autos/<int:pk>/', auto_detail, name='auto-detail'),
    path('api/autos/create/', auto_create, name='auto-create'),
    path('api/autos/<int:pk>/delete/', auto_delete, name='auto-delete'),


    # Маршруты для приложения news
    path('news/', news_views.news_list, name='news_list'),
    path('api/autos/search/', AutoSearchAPIView.as_view(), name='auto-search'),
    # REST API маршруты
    path('api/', include(router.urls)),
    
    # Используем класс AutoListView с методом as_view() для списка автомобилей
    path('api/autos/', AutoListView.as_view(), name='auto-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
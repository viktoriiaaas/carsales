from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars.views import (
    AutoListView, AutoViewSet, filter_cars, index, auto_create, auto_delete, auto_detail
)

from news import views as news_views 

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'autos', AutoViewSet, basename='autos')

urlpatterns = [

    path('', index, name='index'),
    path('admin/', admin.site.urls),

    path('api/autos/filtered-cars/', filter_cars, name='filter-cars'), #Q-запросы
    path('api/news/filtered-news/', news_views.filtered_news, name='filtered-news'), #Q-запросы
    path('api/autos/<int:pk>/', auto_detail, name='auto-detail'),
    path('api/autos/create/', auto_create, name='auto-create'),
    path('api/autos/<int:pk>/delete/', auto_delete, name='auto-delete'),

    path('news/', news_views.news_list, name='news_list'),

    path('api/autos/', AutoListView.as_view(), name='auto-list'),

    path('api/', include(router.urls)),

    # Используем класс AutoListView с методом as_view() для списка автомобилей

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

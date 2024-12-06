from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars import views as cars_views  #  Импорт вью для index.html
from news import views as news_views  #  Импорт вью для news.html
from cars.views import AutoListView
from cars.views import AutoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'autos', AutoViewSet, basename='auto')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', cars_views.index, name='index'),  # Главная страница
    path('news/', news_views.news_list, name='news_list'),  # Страница для новостей
    
    path('api/autos/<int:pk>/', cars_views.auto_detail, name='auto-detail'),  # API для одного автомобиля
    path('api/autos/create/', cars_views.auto_create, name='auto-create'),  # API для создания автомобиля
    path('api/autos/<int:pk>/delete/', cars_views.auto_delete, name='auto-delete'),  # API для удаления автомобиля
    path('api/autos/filtered/', cars_views.filtered_autos, name='filtered-autos'),  # Для фильтрации автомобилей
    path('api/news/filtered/', news_views.filtered_news, name='filtered-news'),  # Для фильтрации новостей

    # Используем класс AutoListView с методом as_view() для списка автомобилей
    path('api/autos/', AutoListView.as_view(), name='auto-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
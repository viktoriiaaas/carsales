from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cars.views import (
    AutoListView, AutoViewSet,  AutoFilterAPIView, AutoSearchAPIView, BrandViewSet, ProfileViewSet, index, auto_create, auto_delete, auto_detail
)
from cars.views import autos_list_view

from news import views as news_views
from django.urls import path
from cars.views import send_test_email
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r'autos', AutoViewSet, basename='autos')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),  # Social Auth
    # Схема API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Redoc (альтернативная документация)
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Главная страница
    path('', index, name='index'),

    # Админка
    path('admin/', admin.site.urls),
    path('api/autos/', AutoListView.as_view(), name='auto-list'),
    path('accounts/', include('allauth.urls')),  # URL-ы для входа/выхода и авторизации
    path('api/autos/filter/', AutoFilterAPIView.as_view(), name='auto-filter'),

    path('api/autos/search/', AutoSearchAPIView.as_view(), name='auto-search'),

    path('api/autos/<int:pk>/', auto_detail, name='auto-detail'),
    path('api/autos/create/', auto_create, name='auto-create'),
    path('api/autos/<int:pk>/delete/', auto_delete, name='auto-delete'),
    
    path('autos/', autos_list_view, name='autos-list'),

    # Маршруты для приложения news
    path('news/', news_views.news_list, name='news_list'),
    path('api/autos/search/', AutoSearchAPIView.as_view(), name='auto-search'),

    path('api/', include(router.urls)),
    path('send-test-email/', send_test_email, name='send_test_email'),  # Новый маршрут

    # Используем класс AutoListView с методом as_view() для списка автомобилей
    path('api/autos/', AutoListView.as_view(), name='auto-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


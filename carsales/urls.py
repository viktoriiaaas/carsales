"""
URL configuration for carsales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cars import views as cars_views  #  Импорт вью для index.html
from news import views as news_views  #  Импорт вью для news.html

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cars_views.index, name='index'),  # Главная страница
    path('news/', news_views.news_list, name='news_list'),  # Страница для новостей
    path('api/autos/', cars_views.auto_list, name='auto-list'),  # API для списка автомобилей
    path('api/autos/<int:pk>/', cars_views.auto_detail, name='auto-detail'),  # API для одного автомобиля
    path('api/autos/create/', cars_views.auto_create, name='auto-create'),  # API для создания автомобиля
    path('api/autos/<int:pk>/delete/', cars_views.auto_delete, name='auto-delete'),  # API для удаления автомобиля
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
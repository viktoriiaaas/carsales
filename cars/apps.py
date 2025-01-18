from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars'

    def ready(self):
        import cars.tasks  # импортируем задачи Celery при загрузке приложения

class CarsConfig(AppConfig):
    name = 'cars'

    def ready(self):
        import cars.signals  # Регистрируем сигналы
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Укажите путь к настройкам Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carsales.settings')

app = Celery('carsales')

# Читаем настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи
app.autodiscover_tasks()

# Убедитесь, что `tasks.py` из `cars` импортируется
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

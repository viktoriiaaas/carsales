from django import template
from cars.models import Auto

register = template.Library()
# 1 простая функция для подсчета общего количества автомобилей
@register.simple_tag
def count_total_autos():
    """
    Возвращает общее количество автомобилей в базе данных.
    """
    return Auto.objects.count()

# 2 подсчет количества объектов на текущей странице (работает с объектами Page)
@register.simple_tag
def count_filtered_autos(page_obj):
    """
    Возвращает количество объектов на текущей странице.
    """
    return len(page_obj) 


# 3 получение последних автомобилей
@register.simple_tag
def get_recent_autos(limit=2):
    """
    Возвращает последние автомобили, ограниченные указанным числом 2
    """
    return Auto.objects.order_by('-created_at')[:limit]
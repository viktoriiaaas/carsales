from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):

# уже есть основные поля для пользователя:
# username (логин),
# password (пароль),
# email,
# first_name и last_name (имя и фамилия),
# is_staff, is_superuser

    phone_num = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='profile_groups',
        blank=True, # пользователь может быть без групп (группы необязательны)
    )
    user_permissions = models.ManyToManyField( 
        'auth.Permission', # user_permissions связывает пользователя с правами доступа 'auth.Permission'
        related_name='profile_permissions',
        blank=True, # пользователь может быть без специальных прав (по умолчанию)
    )

    class Meta:
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})" #user (alexander alexander)


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Автомобильные марки"

    def __str__(self):
        return self.name


class BodyType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Типы кузова"

    def __str__(self):
        return self.name


class EngineType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Типы двигателей"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class SellStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Статусы продажи"

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Местоположение"
        
    def __str__(self):
        return self.name


class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # django автоматически задаст значение этого поля при создании объекта. 
    # после этого его нельзя изменить

    class Meta:
        abstract = True 


class Auto(TimeStamped):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT) 
    # on_delete=models.PROTECT предотвращает удаление бренда, если он связан с автомобилем
    description = models.TextField()
    model = models.CharField(max_length=255)
    year = models.IntegerField(verbose_name="Год выпуска")
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0) # кол-во знаков после запятой
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    sell_status = models.ForeignKey(SellStatus, on_delete=models.PROTECT, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # on_delete=models.CASCADE удаляет автомобиль, если связанный пользователь удалён

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"


class Photo(models.Model):
    url = models.URLField(max_length=700)
    description = models.TextField(blank=False, null=False) # описание = название

    class Meta:
        verbose_name_plural = "Фото"

    def __str__(self):
        return self.description 


class AutoPhoto(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="auto_photos")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Фото автомобилей"

    def __str__(self):
        return f"{self.auto.brand.name} {self.auto.model} ({self.auto.year})"
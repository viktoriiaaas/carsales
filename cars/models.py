from django.db import models
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    phone_num = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='profile_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='profile_permissions',
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


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

    class Meta:
        abstract = True


class Auto(TimeStamped):
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    description = models.TextField()
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    sell_status = models.ForeignKey(SellStatus, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Автомобили"

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"


class Photo(models.Model):
    url = models.URLField(max_length=700)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Фото"

    def __str__(self):
        return self.description or self.url


class AutoPhoto(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name="auto_photos")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Фото автомобилей"

    def __str__(self):
        return f"{self.auto.brand.name} {self.auto.model} ({self.auto.year})"
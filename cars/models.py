from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords

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

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class BodyType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class EngineType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class SellStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    body_type = models.ForeignKey(BodyType, on_delete=models.PROTECT)
    engine_type = models.ForeignKey(EngineType, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    sell_status = models.ForeignKey(SellStatus, on_delete=models.SET_NULL, null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    main_photo = models.ImageField(upload_to='auto_photos/', blank=True, null=True)  # Главное фото автомобиля
    
    history = HistoricalRecords()  # Поле для хранения истории изменений

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"


class Photo(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Дополнительное описание фото

    def __str__(self):
        return self.file_name


class AutoPhoto(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for auto: {self.auto.model}"

from django.db import models
from cars.models import Profile, Photo


class NewCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Категории новостей"

    def __str__(self):
        return self.name

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class New(TimeStamped):
    title = models.CharField(max_length=255)
    content = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(NewCategory, on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class NewPhoto(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name="new_photos")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Фото для новости"

    def __str__(self):
        return f"{self.new.title} - {self.photo.description or 'Фото'}"

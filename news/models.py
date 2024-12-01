from django.db import models
from cars.models import Profile


class NewCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

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
    category = models.ForeignKey(NewCategory, on_delete=models.SET_NULL, null=True)
    main_photo = models.ImageField(upload_to='news_photos/', blank=True, null=True)  # Главное фото новости

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

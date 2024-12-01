from django.contrib import admin

from .models import (
    Profile,
    Brand,
    BodyType,
    EngineType,
    Color,
    SellStatus,
    Region,
    Auto,
    Photo,
    AutoPhoto,
)


# Регистрация моделей с базовой кастомизацией
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_num', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'model', 'year', 'price', 'profile')
    search_fields = ('brand__name', 'model', 'profile__username')
    list_filter = ('brand', 'year')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(BodyType)
admin.site.register(EngineType)
admin.site.register(Color)
admin.site.register(SellStatus)
admin.site.register(Region)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Photo)
admin.site.register(AutoPhoto)

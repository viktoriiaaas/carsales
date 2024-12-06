from django.contrib import admin
from import_export import resources, formats
from import_export.admin import ImportExportModelAdmin
from .models import Auto, AutoPhoto, Profile, Brand, BodyType, EngineType, Color, SellStatus, Region, Photo

# Ресурс для экспорта модели Auto
class AutoResource(resources.ModelResource):
    class Meta:
        model = Auto
        export_order = ('id', 'created_at', 'updated_at', 'brand', 'model', 'year', 'price', 'profile')

# Inline для фотографий автомобиля
class AutoPhotoInline(admin.TabularInline):
    model = AutoPhoto
    extra = 1  # Показать одну пустую форму для добавления новой записи

# Админка для модели Auto с функцией экспорта
class AutoAdmin(ImportExportModelAdmin):
    resource_class = AutoResource
    formats = [formats.base_formats.XLS]  # Поддержка экспорта в Excel формат XLS
    list_display = ('id', 'brand', 'model', 'year', 'display_price', 'profile')
    list_display_links = ('brand', 'model')
    search_fields = ('brand__name', 'model', 'profile__username')
    list_filter = ('brand', 'year')
    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'model', 'year', 'price')
        }),
        ('Дополнительная информация', {
            'fields': ('mileage', 'body_type', 'engine_type', 'color', 'region', 'profile')
        }),
    )
    inlines = [AutoPhotoInline]

    def display_price(self, obj):
        return f"{obj.price} ₽"
    display_price.short_description = 'Цена'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_num', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


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

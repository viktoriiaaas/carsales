from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLS
from .models import Auto, AutoPhoto, Profile, Brand, BodyType, EngineType, Color, SellStatus, Region, Photo


# Экспорт данных модели Auto
class AutoResource(resources.ModelResource):
    brand_name = fields.Field(column_name='Brand Name', readonly=True)
    model_year = fields.Field(column_name='Model Year', readonly=True)

    class Meta:
        model = Auto
        fields = ('id', 'brand_name', 'model', 'model_year', 'price', 'mileage', 'profile__username', 'region__name')
        export_order = ('id', 'brand_name', 'model', 'model_year', 'price', 'mileage', 'profile__username', 'region__name')

    def dehydrate_brand_name(self, auto):
        return auto.brand.name.upper()

    def dehydrate_model_year(self, auto):
        return f"{auto.model} ({auto.year})"


class AutoPhotoInline(admin.TabularInline):
    model = AutoPhoto
    extra = 1
    fields = ['photo']
    autocomplete_fields = ['photo']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['url', 'description']
    search_fields = ['url', 'description']


class AutoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AutoResource
    formats = [XLS]
    list_display = ('id', 'brand', 'model', 'year', 'price', 'profile', 'sell_status')
    list_display_links = ('brand', 'model')
    search_fields = ('brand__name', 'model', 'profile__username', 'sell_status__name')
    list_filter = ('brand', 'year', 'sell_status')
    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'model', 'year', 'price', 'sell_status')
        }),
        ('Дополнительная информация', {
            'fields': ('mileage', 'body_type', 'engine_type', 'color', 'region', 'profile')
        }),
    )
    inlines = [AutoPhotoInline]

    def display_price(self, obj):
        return f"{int(obj.price)} ₽"

    display_price.short_description = 'Цена'


class AutoPhotoAdmin(admin.ModelAdmin):
    list_display = ['auto', 'photo']
    search_fields = ['auto__brand__name', 'auto__model']


admin.site.register(Profile)
admin.site.register(Brand)
admin.site.register(BodyType)
admin.site.register(EngineType)
admin.site.register(Color)
admin.site.register(SellStatus)
admin.site.register(Region)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(AutoPhoto, AutoPhotoAdmin)

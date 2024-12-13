from django.contrib import admin
from import_export import resources, fields, formats
from import_export.admin import ExportMixin
from .models import NewCategory, New, NewPhoto


# Экспорт данных модели New
class NewResource(resources.ModelResource):
    category_name = fields.Field(column_name='Category Name', attribute='category', readonly=True)

    class Meta:
        model = New
        fields = ('id', 'title', 'content', 'profile__username', 'category__name', 'created_at', 'updated_at', 'category_name')
        export_order = ('id', 'title', 'content', 'profile__username', 'category_name', 'created_at', 'updated_at')

    def get_export_queryset(self, queryset, *args, **kwargs):
        # Кастомизация набора данных для экспорта
        return queryset.filter(category__isnull=False)

    def dehydrate_category_name(self, new):
        # Преобразуем имя категории для отображения в экспорте
        return new.category.name if new.category else "Без категории"

    def dehydrate_content(self, new):
        # Обрезаем длинный текст контента
        return new.content[:50] + "..." if len(new.content) > 50 else new.content


# Inline для связи New и Photo через NewPhoto
class NewPhotoInline(admin.TabularInline):
    model = NewPhoto
    extra = 1  # Показать одну пустую строку для добавления связи


# Админка для модели New с функцией экспорта
class NewAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = NewResource
    formats = [formats.base_formats.XLS]  # Поддержка экспорта в Excel формат XLS
    list_display = ('id', 'title', 'profile', 'category', 'created_at')
    search_fields = ('title', 'profile__username', 'category__name')
    list_filter = ('category',)
    inlines = [NewPhotoInline]

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'profile', 'category')
        }),
    )


# админка для категории новостей
class NewCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# Регистрация моделей в админке
admin.site.register(NewCategory, NewCategoryAdmin)
admin.site.register(New, NewAdmin)

from django.contrib import admin
from .models import NewCategory, New, NewPhoto

# inline для связи New и Photo через NewPhoto
class NewPhotoInline(admin.TabularInline):
    model = NewPhoto
    extra = 1  # Показать одну пустую строку для добавления связи


# админка для модели New
class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'profile', 'category', 'created_at')
    search_fields = ('title', 'profile__username', 'category__name')
    list_filter = ('category',)
    inlines = [NewPhotoInline]
    filter_horizontal = ('photos',)  # Добавляем горизонтальный фильтр для фотографий
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'profile', 'category', 'photos')
        }),
    )

# админка для категории новостей
class NewCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# регистрация моделей в админке
admin.site.register(NewCategory, NewCategoryAdmin)
admin.site.register(New, NewAdmin)
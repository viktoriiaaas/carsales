from django.contrib import admin

from .models import ( 
    NewCategory, 
    New )


class NewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'profile', 'category', 'created_at')
    search_fields = ('title', 'profile__username', 'category__name')
    list_filter = ('category',)

class NewCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(NewCategory, NewCategoryAdmin)
admin.site.register(New, NewAdmin)

from rest_framework import serializers
from .models import Auto, Brand
from rest_framework import serializers
from .models import Profile, Auto, Brand

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'phone_num', 'first_name', 'last_name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class AutoSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)  # Вложенный сериализатор для отображения бренда
    profile = ProfileSerializer(read_only=True)  # Вложенный сериализатор для отображения пользователя

    class Meta:
        model = Auto
        fields = [
            'id', 'brand', 'model', 'year', 'description', 'mileage', 
            'price', 'body_type', 'engine_type', 'color', 'region', 
            'sell_status', 'profile', 'main_photo'
        ]

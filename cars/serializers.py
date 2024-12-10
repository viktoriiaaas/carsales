from rest_framework import serializers
from .models import Auto, Brand, Profile

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'phone_num', 'first_name', 'last_name']

class AutoSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Auto
        fields = [
            'id', 'brand', 'model', 'year', 'description', 'mileage', 
            'price', 'body_type', 'engine_type', 'color', 'region', 
            'sell_status', 'profile'
        ]

    def validate_year(self, value):
        if value < 1886 or value > 2024:
            raise serializers.ValidationError("Год выпуска должен быть между 1886 и текущим годом.")
        return value

    def validate_mileage(self, value):
        if value < 0:
            raise serializers.ValidationError("Пробег не может быть отрицательным.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть положительной.")
        return value

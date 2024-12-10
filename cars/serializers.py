from rest_framework import serializers
from .models import Auto, Brand, BodyType, EngineType, Color, Region, SellStatus, Profile
import re


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

    def validate_name(self, value):
        """
        Проверка: название бренда должно быть на латинице.
        """
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("Название бренда должно быть только на латинице.")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'phone_num', 'first_name', 'last_name']


class AutoSerializer(serializers.ModelSerializer):
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )
    body_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BodyType.objects.all(),
        source='body_type',
        write_only=True
    )
    engine_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EngineType.objects.all(),
        source='engine_type',
        write_only=True
    )
    color_id = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        source='color',
        write_only=True
    )
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True
    )
    sell_status_id = serializers.PrimaryKeyRelatedField(
        queryset=SellStatus.objects.all(),
        source='sell_status',
        write_only=True
    )

    class Meta:
        model = Auto
        fields = [
            'id', 'brand', 'brand_id', 'model', 'year', 'description', 'mileage',
            'price', 'body_type', 'body_type_id', 'engine_type', 'engine_type_id',
            'color', 'color_id', 'region', 'region_id', 'sell_status', 'sell_status_id'
        ]

    def validate_price(self, value):
        """
        Проверка цены: минимальная 100, максимальная 1 000 000 000.
        """
        if value < 100:
            raise serializers.ValidationError("Цена автомобиля не может быть ниже 100.")
        if value > 1000000000:
            raise serializers.ValidationError("Цена автомобиля не может быть выше 1 000 000 000.")
        return value

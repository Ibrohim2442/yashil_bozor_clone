from rest_framework import serializers
from .models import Category, Seller


class CategoryChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "image")


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class CategoryDetailSerializer(serializers.ModelSerializer):
    children = CategoryChildSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "image", "children")


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ("id", "name", "description")
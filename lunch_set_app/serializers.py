from rest_framework import serializers

from .models import Dish, LunchSet, ObjectForSetLunch


class LunchSetDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ("id", "title", "slug", "description", "picture")


class ObjectForSetLunchSerializer(serializers.ModelSerializer):
    dish_type = serializers.CharField(source="dish_type.title", read_only=True)
    dish = LunchSetDishSerializer(read_only=True)

    class Meta:
        model = ObjectForSetLunch
        fields = ("id", "dish_type", "dish")


class LunchSetSerializer(serializers.ModelSerializer):
    composition = ObjectForSetLunchSerializer(
        source="objectforsetlunch_set", many=True, read_only=True
    )

    class Meta:
        model = LunchSet
        fields = ("id", "date", "comment", "composition")

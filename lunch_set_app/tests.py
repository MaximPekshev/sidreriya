import datetime

from django.test import TestCase

from .models import Dish, DishesType, LunchSet, ObjectForSetLunch
from .serializers import LunchSetSerializer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_dish_type(title="Суп"):
    return DishesType.objects.create(title=title)


def make_dish(dish_type, title="Борщ"):
    return Dish.objects.create(title=title, dish_type=dish_type)


def make_lunch_set(date=None, comment=""):
    date = date or datetime.date.today()
    return LunchSet.objects.create(date=date, comment=comment)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------

class DishSlugAutoGenerationTest(TestCase):
    """Slug должен заполняться автоматически при первом сохранении."""

    def test_slug_generated_on_create(self):
        dish_type = make_dish_type()
        dish = make_dish(dish_type)
        self.assertTrue(bool(dish.slug), "slug должен быть непустым после сохранения")

    def test_slug_not_overwritten_on_update(self):
        dish_type = make_dish_type()
        dish = make_dish(dish_type)
        original_slug = dish.slug
        dish.title = "Щи"
        dish.save()
        self.assertEqual(dish.slug, original_slug)


# ---------------------------------------------------------------------------
# Serializer tests
# ---------------------------------------------------------------------------

class LunchSetSerializerTest(TestCase):
    def setUp(self):
        self.dish_type = make_dish_type("Первое")
        self.dish = make_dish(self.dish_type, "Борщ")
        self.lunch = make_lunch_set(comment="Тест")
        ObjectForSetLunch.objects.create(
            dish_type=self.dish_type,
            dish=self.dish,
            lunch_set=self.lunch,
        )

    def test_contains_expected_fields(self):
        data = LunchSetSerializer(self.lunch).data
        self.assertIn("id", data)
        self.assertIn("date", data)
        self.assertIn("comment", data)
        self.assertIn("composition", data)

    def test_composition_has_correct_structure(self):
        data = LunchSetSerializer(self.lunch).data
        self.assertEqual(len(data["composition"]), 1)
        item = data["composition"][0]
        self.assertEqual(item["dish_type"], "Первое")
        self.assertIn("dish", item)
        self.assertEqual(item["dish"]["title"], "Борщ")

    def test_empty_composition(self):
        empty_lunch = make_lunch_set(date=datetime.date(2026, 1, 1))
        data = LunchSetSerializer(empty_lunch).data
        self.assertEqual(data["composition"], [])


# API-тесты находятся в API/tests.py

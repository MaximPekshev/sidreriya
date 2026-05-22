import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from lunch_set_app.models import Dish, DishesType, LunchSet, ObjectForSetLunch


def make_dish_type(title="Суп"):
    return DishesType.objects.create(title=title)


def make_dish(dish_type, title="Борщ"):
    return Dish.objects.create(title=title, dish_type=dish_type)


def make_lunch_set(date=None, comment=""):
    date = date or datetime.date.today()
    return LunchSet.objects.create(date=date, comment=comment)


class LunchSetAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dish_type = make_dish_type("Второе")
        self.dish = make_dish(self.dish_type, "Котлета")
        self.today = datetime.date.today()
        self.lunch = make_lunch_set(date=self.today)
        ObjectForSetLunch.objects.create(
            dish_type=self.dish_type,
            dish=self.dish,
            lunch_set=self.lunch,
        )

    def test_list_returns_200(self):
        response = self.client.get("/api/v2/lunch-set/")
        self.assertEqual(response.status_code, 200)

    def test_list_returns_lunch_sets(self):
        response = self.client.get("/api/v2/lunch-set/")
        self.assertEqual(len(response.data), 1)

    def test_detail_returns_200(self):
        response = self.client.get(f"/api/v2/lunch-set/{self.today}/")
        self.assertEqual(response.status_code, 200)

    def test_detail_contains_composition(self):
        response = self.client.get(f"/api/v2/lunch-set/{self.today}/")
        self.assertIn("composition", response.data)
        self.assertEqual(len(response.data["composition"]), 1)
        self.assertEqual(response.data["composition"][0]["dish"]["title"], "Котлета")

    def test_detail_not_found(self):
        response = self.client.get("/api/v2/lunch-set/2000-01-01/")
        self.assertEqual(response.status_code, 404)

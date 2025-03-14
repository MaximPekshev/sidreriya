from django.db.models import QuerySet
from django.http import HttpRequest
import json
from wishlistapp.services import wishlist_object
from goodapp.models import Good

def json_goods_list_from_page_object_list(request: HttpRequest, page_object_list: QuerySet) -> list:
    goods_list = []
    wishlist = wishlist_object(request)
    for item in page_object_list:
        imgObj = item.main_image()
        discount_price = item.discount_price()
        goods_list.append({
            'pk': item.pk,
            'slug': item.slug,
            'name': item.name,
            'name_en': item.name_en,
            'quantity': int(item.quantity),
            'price': int(item.price),
            'old_price': int(item.old_price) if item.old_price else None,
            'discount_price': int(discount_price) if discount_price else None,
            'img': imgObj.images.url if imgObj else None, 
            'categoryName': item.category.name,
            'is_vine': item.is_vine,
            'is_cidre': item.is_cidre,
            'in_barrel': item.in_barrel,
            'loading': False,
            'in_wishlist': True if item in wishlist.items() else False
        })
    return json.dumps(goods_list)

def json_good_from_object(request: HttpRequest, good_object: Good) -> dict:
    wishlist = wishlist_object(request)
    return json.dumps({
        'pk': good_object.pk,
        'slug': good_object.slug,
        'name': good_object.name,
        'name_en': good_object.name_en,
        'quantity': int(good_object.quantity),
        'price': int(good_object.price),
        'old_price': int(good_object.old_price) if good_object.old_price else None,
        'discount_price': int(good_object.discount_price()) if good_object.discount_price() else None,
        'img': good_object.main_image().images.url if good_object.main_image() else None, 
        'categoryName': good_object.category.name,
        'is_vine': good_object.is_vine,
        'is_cidre': good_object.is_cidre,
        'in_barrel': good_object.in_barrel,
        'loading': False,
        'in_wishlist': True if good_object in wishlist.items() else False
    })
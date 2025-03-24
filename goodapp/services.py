import json
from wishlistapp.services import wishlist_object
from cartapp.services import cart_object

def json_goods_list_from_page_object_list(request, page_object_list):
    goods_list = []
    wishlist = wishlist_object(request)
    cart = cart_object(request)
    for item in page_object_list:
        imgObj = item.main_image()
        discount_price = item.discount_price()
        good = {
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
            'wl_loading': False,
            'ct_loading': False,
        }
        if wishlist:
            try:
                good['in_wishlist'] = True if item in wishlist.items() else False
            except:
                pass
        try:
            cartinfo = cart.items().get(good=item)
            cart_item_discount_price = cartinfo.discount_price()
            cart_item_discount_summ = cartinfo.discount_summ()
            good['cartInfo'] = {
                'quantity': int(cartinfo.quantity),
                'price': int(cartinfo.price),
                'discount_price': int(cart_item_discount_price) if cart_item_discount_price else None,
                'summ': int(cartinfo.summ),
                'discount_summ': int(cart_item_discount_summ) if cart_item_discount_summ else None
            }
        except:
            pass
        goods_list.append(good)
    return json.dumps(goods_list)

def json_good_from_object(request, good_object):
    wishlist = wishlist_object(request)
    cart = cart_object(request)
    good = {
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
        'wl_loading': False,
        'ct_loading': False,
    }
    if wishlist:
        try:
            good['in_wishlist'] = True if good_object in wishlist.items() else False
        except:
            pass
    try:
        cartinfo = cart.items().get(good=good_object)
        cart_item_discount_price = cartinfo.discount_price()
        cart_item_discount_summ = cartinfo.discount_summ()
        good['cartInfo'] = {
            'quantity': int(cartinfo.quantity),
            'price': int(cartinfo.price),
            'discount_price': int(cart_item_discount_price) if cart_item_discount_price else None,
            'summ': int(cartinfo.summ),
            'discount_summ': int(cart_item_discount_summ) if cart_item_discount_summ else None
        }
    except:
        pass
    return json.dumps(good)

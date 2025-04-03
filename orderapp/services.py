from orderapp.models import Order_Item
import datetime
from django.utils import timezone
from django.db.models import Sum

def popular_order_items():
    date_to = timezone.now()
    date_from = date_to - datetime.timedelta(days=30)
    """
    Возвращает список популярных товаров за указанный период
    :param date_from: Дата начала периода
    :param date_to: Дата конца периода
    :return: Список популярных товаров
    """
    order_items = Order_Item.objects.filter(
            order__date__range=(date_from, date_to)
        ).exclude(
            good__category__name__in = ['Куличи', 'Вареники', 'Сертификаты']
        ).exclude(
            good__name = 'Дружеский обед'
        )
    drinks_with_qty = {}
    dishes_with_qty = {}
    for item in order_items:
        qty = order_items.filter(good=item.good).aggregate(Sum('quantity'))['quantity__sum']
        obj = {
            'good': item.good,
            'quantity': int(qty)
        }
        if item.good.is_cidre or item.good.is_vine:
            if item.good.slug not in drinks_with_qty:
                drinks_with_qty[item.good.slug] = obj
        else:
            if item.good.slug not in dishes_with_qty:
                dishes_with_qty[item.good.slug] = obj
    drinks_with_qty = dict(sorted(drinks_with_qty.items(), key=lambda kv: kv[1]['quantity'], reverse=True))
    dishes_with_qty = dict(sorted(dishes_with_qty.items(), key=lambda kv: kv[1]['quantity'], reverse=True))
    return {
        'drinks': dict(list(drinks_with_qty.items())[:6]),
        'dishes': dict(list(dishes_with_qty.items())[:6])
    }
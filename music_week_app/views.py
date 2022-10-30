from django.shortcuts import render
import datetime
from django.db.models import Sum
from cartapp.views import get_cart
from wishlistapp.views import get_wishlist
from goodapp.views import  get_in_barrels
from cartapp.models import Cart_Item
from wishlistapp.models import Wishlist_Item
from .models import MusicWeek

def show_actual_music_week(request):

    music_week = MusicWeek.objects.filter(date__lte=datetime.datetime.now()).order_by('date').last()

    context = {
        'music_week': music_week,
		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))),
	}

    return  render(request, 'music_week_app/actual_music_week.html', context)
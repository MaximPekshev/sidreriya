from django.shortcuts import render
from cartapp.views import get_cart
from wishlistapp.views import get_wishlist
from goodapp.views import  get_in_barrels
from cartapp.models import Cart_Item
from wishlistapp.models import Wishlist_Item
from django.db.models import Sum
from .models import Festival

def show_festival_list(request):
	context = {
		'festivals': Festival.objects.filter(is_active=True).order_by('id')[:2],
		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return render(request, 'festapp/fest_list.html', context)


def show_festival(request, cpu_slug):


	context = {
		'festival': Festival.objects.filter(cpu_slug=cpu_slug).first(),
		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return render(request, 'festapp/fest.html', context)
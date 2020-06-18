from django.shortcuts import render
from goodapp.models import Category, In_Barrels, Picture
from cartapp.models import Cart, Cart_Item
from cartapp.views import get_cart
from goodapp.views import Item, get_in_barrels


def show_index(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	return  render(request, 'baseapp/index.html', context)

def show_delivery(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	return  render(request, 'baseapp/delivery.html', context)	

def show_atmosphere(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	return  render(request, 'baseapp/atmosphere.html', context)

def show_about_us(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	return  render(request, 'baseapp/about_us.html', context)	

def show_contact_us(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	return  render(request, 'baseapp/contact_us.html', context)


def show_wishlist(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	return  render(request, 'baseapp/wishlist.html', context)
		
from django.shortcuts import render
from goodapp.models import Category, In_Barrels, Picture, Set_Lunch
from goodapp.models import Bestseller
from cartapp.models import Cart, Cart_Item
from wishlistapp.models import Wishlist, Wishlist_Item
from cartapp.views import get_cart
from wishlistapp.views import get_wishlist
from goodapp.views import Item, get_in_barrels
from goodapp.views import get_items_with_pictures
from django.db.models import Sum

import datetime
from authapp.models import Buyer


def show_index(request):

	bestsellsers = []

	for good in Bestseller.objects.all().order_by('?'):
		bestsellsers.append(good.good)


	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))),
		'bestsellers' : get_items_with_pictures(bestsellsers),

	}

	return  render(request, 'baseapp/index.html', context)

def show_delivery(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return  render(request, 'baseapp/delivery.html', context)	

def show_atmosphere(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return  render(request, 'baseapp/atmosphere.html', context)

def show_about_us(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return  render(request, 'baseapp/about_us.html', context)	

def show_contact_us(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return  render(request, 'baseapp/contact_us.html', context)


def show_wishlist(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return  render(request, 'baseapp/wishlist.html', context)
		
def show_promo(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

	}

	return  render(request, 'baseapp/promo_obedy.html', context)

def show_set_lunch(request):

	now = datetime.datetime.now()

	min_time = '11:00'
	max_time = '18:00'

	min_time_datetime = now.replace(hour=11, minute=0)
	max_time_datetime = now.replace(hour=18, minute=0)

	now_active = False

	if min_time_datetime < now < max_time_datetime:
		now_active = True
		if now < (max_time_datetime - datetime.timedelta(minutes=30)):
			min_time = (now + datetime.timedelta(minutes=30)).strftime('%H:%M')
		else:
			min_time = max_time


	set_lunch = Set_Lunch.objects.filter(date=now).first()


	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))),
		'min_time': min_time,
		'max_time': max_time,
		'now_active': now_active,
		'set_lunch': set_lunch,

	}


	if request.user.is_authenticated: 

		try:

			buyer = Buyer.objects.get(user=request.user)

			context.update({

				'buyer': buyer,

				})

		except Buyer.DoesNotExist:

			pass


	return  render(request, 'baseapp/set_lunch.html', context)


def show_gift_boxes(request):
	


	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))),

	}

	if request.user.is_authenticated: 

		try:

			buyer = Buyer.objects.get(user=request.user)

			context.update({

				'buyer': buyer,

				})

		except Buyer.DoesNotExist:

			pass

	return  render(request, 'baseapp/gift_boxes.html', context)


def show_breakfasts(request):
	
	bestsellsers = []

	for good in Bestseller.objects.all().order_by('?'):
		bestsellsers.append(good.good)
	

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))),
		'bestsellers' : get_items_with_pictures(bestsellsers),

	}

	if request.user.is_authenticated: 

		try:

			buyer = Buyer.objects.get(user=request.user)

			context.update({

				'buyer': buyer,

				})

		except Buyer.DoesNotExist:

			pass

	return  render(request, 'baseapp/breakfasts.html', context)	
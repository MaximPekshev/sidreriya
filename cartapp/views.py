from django.shortcuts import render, redirect
from .models import Cart, Cart_Item
from goodapp.models import Good, Picture, In_Barrels
from .models import cart_calculate_summ
from authapp.models import Buyer
from goodapp.views import get_in_barrels
from django.db.models import Sum
from wishlistapp.views import get_wishlist
from wishlistapp.models import Wishlist, Wishlist_Item
from decimal import Decimal

import datetime


class Item(object):
	
	good 	= Good
	image 	= Picture


def get_cart(request):

	if request.user.is_authenticated:
		cart 		= Cart.objects.filter(user = request.user).last()
	else:
		cart_id 	= request.session.get("cart_id")	
		cart 		= Cart.objects.filter(id = cart_id).last()

	return cart

def create_cart(request):

	cart_id 		= request.session.get("cart_id")
	cart 			= Cart()

	if request.user.is_authenticated:
		cart.user = request.user
	else:
		cart.user = None

	cart.save()
	request.session['cart_id'] = cart.id

	return cart


def show_cart(request):

	cart  = get_cart(request)

	table = []

	if cart != None:

		cart_items 	 = Cart_Item.objects.filter(cart = cart)

		for item in cart_items:

			cr_item = Item()

			cr_item.price = item.price

			cr_item.quantity = item.quantity

			cr_item.summ = item.summ
		
			cr_item.good = item.good
			cr_item.cart_item = item
			
			images = Picture.objects.filter(good=item.good, main_image=True).first()

			images = images if images else Picture.objects.filter(good=item.good).first()

			cr_item.image = images
		 	
			table.append(cr_item)


	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)

	context = {
		'cart_items': table, 
		'cart': cart , 
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		}
	
	return render(request, 'cartapp/cart_page.html', context)


def cart_add_item(request, slug):

	if request.method == 'POST':

		quantity 		= Decimal(request.POST.get('quantity'))

		cart 			= get_cart(request)

		if cart == None:

			cart = create_cart(request)

		good 				= Good.objects.get(slug = slug)
		item 				= Cart_Item.objects.filter(cart=cart, good=good).first()
		if item is None:	
			item 			= Cart_Item(cart = cart, good = good, quantity = quantity, price = good.price)
		else:			
			item.quantity	+= quantity

		item.save()

		current_path = request.META['HTTP_REFERER']
		return redirect(current_path)

def cart_del_item(request, slug):

	cart 	= get_cart(request)

	if cart != None:

		good 	= Good.objects.get(slug = slug)
		item 	= Cart_Item.objects.filter(cart = cart, good = good).first().delete()
		cart_calculate_summ(cart)


	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)

def cart_checkout(request):

	weekday = datetime.datetime.weekday(datetime.datetime.today())

	now = datetime.datetime.now()

	if weekday == 5 or weekday == 4:
		min_time = '09:00'
		max_time = '2:30'

		if  now.replace(hour=0, minute=0) < now < now.replace(hour=2, minute=30):

			min_time_datetime = now.replace(hour=0, minute=0)
			max_time_datetime = now.replace(hour=2, minute=30)

		else:	

			min_time_datetime = now.replace(hour=9, minute=0)
			max_time_datetime = now.replace(hour=23, minute=59, second=59)
	else:
		min_time = '12:00'
		max_time = '23:30'

		min_time_datetime = now.replace(hour=12, minute=0)
		max_time_datetime = now.replace(hour=23, minute=30)

	now_active = False

	if min_time_datetime < now < max_time_datetime:
		now_active = True
		if now < (max_time_datetime - datetime.timedelta(minutes=30)):
			min_time = (now + datetime.timedelta(minutes=30)).strftime('%H:%M')
		else:
			min_time = max_time	

	cart  = get_cart(request)

	if cart != None:

		cart_items 	 = Cart_Item.objects.filter(cart = cart)

	context = {
		'cart_items': cart_items, 
		'cart': cart , 
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		'min_time': min_time,
		'max_time': max_time,
		'now_active': now_active,
		}


	if request.user.is_authenticated: 

		try:

			buyer = Buyer.objects.get(user=request.user)

			context.update({

				'buyer': buyer,

				})

		except Buyer.DoesNotExist:

			pass
	
	
	return render(request, 'cartapp/checkout.html', context)	
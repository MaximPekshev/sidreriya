from django.shortcuts import (
    render, 
    redirect
)
from decimal import Decimal
import datetime

from cartapp.models import (
    Cart, 
    Cart_Item,
	cart_calculate_summ
)
from goodapp.models import (
    Good, 
    In_Barrels
)
from authapp.models import Buyer

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

	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)
	context = {
		'barrels': barrels,
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
		free_cart_items = []
		cart_items = Cart_Item.objects.filter(cart = cart)
		for item in cart_items:
			if item.good.quantity != 0:
				free_cart_items.append(item)

	context = {
		'cart_items': free_cart_items, 
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
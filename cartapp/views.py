from django.shortcuts import render, redirect
from .models import Cart, Cart_Item
from goodapp.models import Good, Picture 
from .models import cart_calculate_summ
from authapp.models import Buyer
from goodapp.views import get_in_barrels


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
			
			images = Picture.objects.filter(good=item.good, main_image=True).first()

			images = images if images else Picture.objects.filter(good=item.good).first()

			cr_item.image = images
		 	
			table.append(cr_item)


	context = {
		'cart_items': table, 
		'cart': cart , 
		'cart_count': len(Cart_Item.objects.filter(cart=cart)),
		'in_bar': get_in_barrels(),
		}
	
	return render(request, 'cartapp/cart_page.html', context)


def cart_add_item(request, slug):

	if request.method == 'POST':

		quantity 		= int(request.POST.get('quantity'))

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

	cart  = get_cart(request)

	if cart != None:

		cart_items 	 = Cart_Item.objects.filter(cart = cart)

	context = {
		'cart_items': cart_items, 
		'cart': cart , 
		'cart_count': len(Cart_Item.objects.filter(cart=cart)),
		'in_bar': get_in_barrels(),
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
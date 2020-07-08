from django.shortcuts import render, redirect
from goodapp.models import Good, Picture
from .models import Wishlist, Wishlist_Item
from cartapp.models import Cart, Cart_Item
# from goodapp.views import get_in_barrels
# from cartapp.views import get_cart
from django.db.models import Sum
from goodapp.models import In_Barrels




class Item(object):
	
	good 	= Good
	image 	= Picture


def get_in_barrels():

	in_bar = In_Barrels.objects.all()[:8]

	table = []

	for good in in_bar:

		item = Item()

		item.good = good.good
		
		images = Picture.objects.filter(good=good.good, main_image=True).first()
		if images:
			item.image = images
		else:
			item.image = Picture.objects.filter(good=good.good).first()
		 	
		table.append(item)

	return table

def get_cart(request):

	if request.user.is_authenticated:
		cart 		= Cart.objects.filter(user = request.user).last()
	else:
		cart_id 	= request.session.get("cart_id")	
		cart 		= Cart.objects.filter(id = cart_id).last()

	return cart


def get_wishlist(request):

	if request.user.is_authenticated:
		wishlist 	= Wishlist.objects.filter(user = request.user).last()
	else:
		wishlist_id = request.session.get("wishlist_id")	
		wishlist 	= Wishlist.objects.filter(id = wishlist_id).last()

	return wishlist


def create_wishlist(request):

	wishlist_id 	= request.session.get("wishlist_id")
	wishlist		= Wishlist()

	if request.user.is_authenticated:
		wishlist.user = request.user
	else:
		wishlist.user = None

	wishlist.save()
	request.session['wishlist_id'] = wishlist.id

	return wishlist


def show_wishlist(request):

	wishlist = get_wishlist(request)

	table = []

	if wishlist != None:

		for item in  Wishlist_Item.objects.filter(wishlist=wishlist):
			
			wl_item = Item()

			wl_item.price = item.price
			wl_item.good = item.good
			images = Picture.objects.filter(good=item.good, main_image=True).first()
			wl_item.image = images if images else Picture.objects.filter(good=item.good).first()

			table.append(wl_item)

	context = {

		'wishlist_items': table,
		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count': len(table),


	}


	return render(request, 'wishlistapp/wishlist.html', context)



def wishlist_add_item(request, slug):

	wishlist = get_wishlist(request)

	if wishlist == None:

		wishlist = create_wishlist(request)

	good 	= Good.objects.get(slug = slug)
	item 	= Wishlist_Item.objects.filter(wishlist=wishlist, good=good).first()
	if item:
		item.delete()
	else:			
		item 	= Wishlist_Item(wishlist = wishlist, good = good, price = good.price)
		item.save()

	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)
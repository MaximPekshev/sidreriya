from django.shortcuts import render, redirect
from goodapp.models import (
    Good
)
from wishlistapp.models import (
    Wishlist, 
	Wishlist_Item
)


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
	return render(request, 'wishlistapp/wishlist.html')

def wishlist_add_item(request, slug):

	if request.user.is_authenticated:
		wishlist 	= Wishlist.objects.filter(user = request.user).last()
	else:
		wishlist_id = request.session.get("wishlist_id")	
		wishlist 	= Wishlist.objects.filter(id = wishlist_id).last()

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
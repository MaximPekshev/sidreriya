from wishlistapp.models import Wishlist
from django.http import HttpRequest

def wishlist_object(request: HttpRequest) -> Wishlist:
	if request.user.is_authenticated:
		wishlist 	= Wishlist.objects.filter(user = request.user).last()
	else:
		wishlist_id = request.session.get("wishlist_id")	
		wishlist 	= Wishlist.objects.filter(id = wishlist_id).last()
	return wishlist

def create_wishlist(request: HttpRequest) -> Wishlist:
	wishlist		= Wishlist()
	if request.user.is_authenticated:
		wishlist.user = request.user
	else:
		wishlist.user = None
	wishlist.save()
	request.session['wishlist_id'] = wishlist.id
	return wishlist
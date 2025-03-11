from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from wishlistapp.services import (
    wishlist_object,
	create_wishlist
)
from goodapp.models import (
    Good
)
from wishlistapp.models import ( 
	Wishlist_Item
)

class WishlistView(View):
	
	def get(self, request: HttpRequest) -> HttpResponse:
		context = {
			'wishlist_object': wishlist_object(request),
		}
		return render(request, 'wishlistapp/wishlist.html', context)	

def wishlist_add_item(request, slug):

	wishlist = wishlist_object(request)
	if wishlist == None:
		wishlist = create_wishlist(request)
	try:
		good = Good.objects.get(slug = slug)
	except Good.DoesNotExist:
		pass
	item = Wishlist_Item.objects.filter(wishlist=wishlist, good=good).first()
	if item:
		item.delete()
	else:			
		item = Wishlist_Item(
			wishlist = wishlist, 
			good = good, 
			price = good.price
		)
		item.save()
	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)
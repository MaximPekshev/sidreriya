from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from wishlistapp.services import (
    wishlist_object,
	create_wishlist
)
from wishlistapp.models import ( 
	Wishlist_Item
)
from goodapp.models import (
    Good
)
from goodapp.services import (
	json_goods_list_from_page_object_list
)

class WishlistView(View):
	
	def get(self, request: HttpRequest) -> HttpResponse:
		wishlist = wishlist_object(request)
		context = {
			'wishlist_object': wishlist,
			'goods_list': json_goods_list_from_page_object_list(request, wishlist.items()),
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
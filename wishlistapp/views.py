from django.shortcuts import render
from django.views.generic import View
from wishlistapp.services import (
    wishlist_object,
	create_wishlist
)
from goodapp.services import (
	json_goods_list_from_page_object_list
)

class WishlistView(View):
	
	def get(self, request):
		wishlist = wishlist_object(request)
		if wishlist == None:
			wishlist = create_wishlist(request)
		context = {
			'goods_list': json_goods_list_from_page_object_list(request, wishlist.items()),
		}
		return render(request, 'wishlistapp/wishlist.html', context)
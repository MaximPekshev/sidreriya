from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import View
from wishlistapp.services import (
    wishlist_object,
)
from goodapp.services import (
	json_goods_list_from_page_object_list
)

class WishlistView(View):
	
	def get(self, request: HttpRequest) -> HttpResponse:
		wishlist = wishlist_object(request)
		context = {
			'goods_list': json_goods_list_from_page_object_list(request, wishlist.items()),
		}
		return render(request, 'wishlistapp/wishlist.html', context)
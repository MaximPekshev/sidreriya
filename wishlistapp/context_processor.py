from wishlistapp.services import wishlist_object
def wishlist(request):
	return {
		'wishlist': wishlist_object(request)
	}
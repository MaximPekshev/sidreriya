from wishlistapp.models import Wishlist
def wishlist(request):
	if request.user.is_authenticated:
		wishlist 	= Wishlist.objects.filter(user = request.user).last()
	else:
		wishlist_id = request.session.get("wishlist_id")	
		wishlist 	= Wishlist.objects.filter(id = wishlist_id).last()
	return {
		'wishlist': wishlist
	}
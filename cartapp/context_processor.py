from cartapp.models import Cart

def cart(request): 
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user = request.user).last()
	else:
		cart_id = request.session.get("cart_id")	
		cart = Cart.objects.filter(id = cart_id).last()
	return {
        'cart': cart
	}
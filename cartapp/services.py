from cartapp.models import Cart
from django.http import HttpRequest

def cart_object(request: HttpRequest) -> Cart:
	if request.user.is_authenticated:
		cart = Cart.objects.filter(user = request.user).last()
	else:
		cart_id = request.session.get("cart_id")
		cart = Cart.objects.filter(id = cart_id).last()
	return cart

def create_cart(request: HttpRequest) -> Cart:
	cart 			= Cart()
	if request.user.is_authenticated:
		cart.user = request.user
	else:
		cart.user = None
	cart.save()
	request.session['cart_id'] = cart.id
	return cart

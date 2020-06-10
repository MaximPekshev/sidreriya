from django.urls import path
from .views import show_cart
from .views import cart_add_item
from .views import cart_del_item
from .views import cart_checkout


urlpatterns = [

	path('',				show_cart, name='show_cart'),
	path('checkout/', 		cart_checkout, name='cart_checkout'),
	path('add/<str:slug>/', cart_add_item, name='cart_add_item'),
	path('del/<str:slug>/', cart_del_item, name='cart_del_item'),

]

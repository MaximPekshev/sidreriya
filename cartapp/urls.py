from django.urls import path
from .views import cart_add_item
from .views import cart_del_item
from .views import cart_checkout

from cartapp.views import (
    CartView
)


urlpatterns = [

	path('', CartView.as_view(), name='show_cart'),
    
	path('checkout/', 		cart_checkout, name='cart_checkout'),
	path('add/<str:slug>/', cart_add_item, name='cart_add_item'),
	path('del/<str:slug>/', cart_del_item, name='cart_del_item'),

]

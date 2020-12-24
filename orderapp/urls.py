from django.urls import path
from .views import show_orders, order_add, sendmail



urlpatterns = [

	path('',				show_orders, name='show_orders'),
	path('add/', 			order_add, name='order_add'),
	path('sendmail/', 			sendmail, name='sendmail'),


]

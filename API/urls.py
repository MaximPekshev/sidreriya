from django.urls import path
from .views import GoodView, SingleGoodView, OrderView, SingleOrderView
from .views import Order_ItemsView

urlpatterns = [

	path('goods/', 						GoodView.as_view()),
	path('goods/<str:good_uid>', 		SingleGoodView.as_view()),
	path('orders/', 					OrderView.as_view()),
	path('orders/<str:order_number>', 	SingleOrderView.as_view()),
	path('order-items/<str:order_number>', 	Order_ItemsView.as_view()),
]

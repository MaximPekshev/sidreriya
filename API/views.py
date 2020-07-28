from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView,ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from goodapp.serializers import GoodSerializer
from orderapp.serializers import OrderSerializer, Order_ItemSerializer

from goodapp.models import Good
from orderapp.models import Order, Order_Item

class GoodView(ListAPIView):

	queryset = Good.objects.all()
	serializer_class = GoodSerializer

class SingleGoodView(RetrieveUpdateAPIView):
	
	queryset = Good.objects.all()
	serializer_class = GoodSerializer
	lookup_field = 'good_uid'

	def get_object(self):
		good_uid = self.kwargs["good_uid"]
		return get_object_or_404(Good, good_uid=good_uid)

class OrderView(ListAPIView):

	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class SingleOrderView(RetrieveUpdateAPIView):
	
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	lookup_field = 'order_number'

	def get_object(self):
		order_number = self.kwargs["order_number"]
		return get_object_or_404(Order, order_number=order_number)	

		
class Order_ItemsView(ListAPIView):

	serializer_class = Order_ItemSerializer
	lookup_field = 'order_number'

	def get_queryset(self):
		order_number = self.kwargs["order_number"]
		order = get_object_or_404(Order, order_number=order_number)
		return Order_Item.objects.filter(order=order)
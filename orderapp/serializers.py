from rest_framework import serializers
from orderapp.models import (
    Order, 
	Order_Item
)

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ('pk', 'date', 'summ','buyer', 'order_number', 'address', 'cook_time', 'first_name', 'last_name', 'phone', 'email')
    		
class Order_ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order_Item
		fields = ('order', 'good','quantity', 'price', 'summ')    		
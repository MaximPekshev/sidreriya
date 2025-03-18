from rest_framework import serializers
from cartapp.models import Cart_Item
from cartapp.services import (
    cart_object, 
    create_cart
)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_Item
        fields = ('id', 'good', 'price', 'quantity')
    def create(self, validated_data):
        request = self.context.get("request")
        cart = cart_object(request)
        if not cart:
            cart = create_cart(request)
        ct_item = Cart_Item.objects.filter(cart=cart, good=validated_data.get('good')).first()
        if not ct_item:
            return Cart_Item.objects.create(
                **validated_data,
                cart=cart
            )
        else:
            ct_item.quantity += validated_data.get('quantity')
            ct_item.save()
            return ct_item
    def delete(self, validated_data, slug):
        request = self.context.get("request")
        cart = cart_object(request)
        if not cart:
            cart = create_cart(request)
        ct_item = Cart_Item.objects.filter(cart=cart, good__slug=slug).first()
        if ct_item:
            ct_item.delete()

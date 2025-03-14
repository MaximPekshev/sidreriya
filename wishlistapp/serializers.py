from rest_framework import serializers
from wishlistapp.models import Wishlist_Item
from wishlistapp.services import wishlist_object, create_wishlist

class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist_Item
        fields = ('id', 'good', 'price')
    def create(self, validated_data):
        request = self.context.get("request")
        wishlist = wishlist_object(request)
        if not wishlist:
            wishlist = create_wishlist(request) 
        wl_item = Wishlist_Item.objects.filter(wishlist=wishlist, good=validated_data.get('good')).first()
        if not wl_item:
            return Wishlist_Item.objects.create(
                **validated_data,
                wishlist=wishlist
            )
        else:
            return wl_item
    def delete(self, validated_data, slug):
        request = self.context.get("request")
        wishlist = wishlist_object(request)
        if not wishlist:
            wishlist = create_wishlist(request) 
        wl_item = Wishlist_Item.objects.filter(wishlist=wishlist, good__slug=slug).first()
        if wl_item:
            wl_item.delete()
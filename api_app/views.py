from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from wishlistapp.serializers import WishListItemSerializer
from wishlistapp.models import Wishlist_Item
from wishlistapp.services import wishlist_object 

from cartapp.serializers import CartItemSerializer
from cartapp.models import Cart_Item
from cartapp.services import cart_object


class WishlistItemsList(generics.CreateAPIView):
    serializer_class = WishListItemSerializer
    queryset = Wishlist_Item.objects.all()

class WishlistItemDetail(APIView):
    def delete(self, request, slug, format=None):
        wishlist = wishlist_object(request)
        snippet = Wishlist_Item.objects.filter(wishlist=wishlist, good__slug=slug).first()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemsList(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = Cart_Item.objects.all()

class CartItemDetail(APIView):
    def delete(self, request, slug, format=None):
        cart = cart_object(request)
        snippet = Cart_Item.objects.filter(cart=cart, good__slug=slug).first()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

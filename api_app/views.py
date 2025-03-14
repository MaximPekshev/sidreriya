# from django.shortcuts import render
# from django.http import HttpRequest, HttpResponse  
from wishlistapp.services import wishlist_object 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wishlistapp.serializers import WishListItemSerializer
from wishlistapp.models import Wishlist_Item
from rest_framework import generics

class WishlistItemsList(generics.ListCreateAPIView):
    serializer_class = WishListItemSerializer
    queryset = Wishlist_Item.objects.all()

class WishlistItemDetail(APIView):
    def delete(self, request, slug, format=None):
        wishlist = wishlist_object(request)
        snippet = Wishlist_Item.objects.filter(wishlist=wishlist, good__slug=slug).first()
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
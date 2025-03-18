from django.urls import path

from api_app.views import (
    WishlistItemsList, 
    WishlistItemDetail,
    CartItemsList,
    CartItemDetail
)

app_name = "api_app"

urlpatterns = [
    path('wishlist/', WishlistItemsList.as_view()),
    path('wishlist/<str:slug>/', WishlistItemDetail.as_view()),
    path('cart/', CartItemsList.as_view()),
    path('cart/<str:slug>/', CartItemDetail.as_view()),
]
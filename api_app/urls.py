from django.urls import path

from api_app.views import (
    WishlistItemsList, 
    WishlistItemDetail 
)

app_name = "api_app"

urlpatterns = [
    path('wishlist/', WishlistItemsList.as_view()),
    path('wishlist/<str:slug>/', WishlistItemDetail.as_view()),
]
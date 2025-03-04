from django.urls import path
from goodapp.views import (
    CatalogView,
    InBarrelsView,
    GoodView,
    CategoryView
)

urlpatterns = [
	path('', CatalogView.as_view(), name='show_catalog'),
	path('in-barrels/', InBarrelsView.as_view(), name='show_in_barrels'),
	path('category/<str:slug>/', CategoryView.as_view(), name='show_category'),
	path('<str:slug>/', GoodView.as_view(), name='show_good'),
]

from django.urls import path
from goodapp.views import (
    CatalogView,
    SearchView,
    ManufacturerView,
    InBarrelsView,
    GoodView,
    CategoryView,
    FilteredGoodsView,
    TagView,
    # show_product_with_tag,
    # show_product_with_filters,
)

urlpatterns = [
	path('', CatalogView.as_view(), name='show_catalog'),
	path('search/', SearchView.as_view(), name='show_search_result'),
	path('show-tag/', TagView.as_view(), name='show_product_with_tag'),
	path('filter/', FilteredGoodsView.as_view(), name='show_product_with_filters'),
	path('in-barrels/', InBarrelsView.as_view(), name='show_in_barrels'),
	path('category/<str:slug>/', CategoryView.as_view(), name='show_category'),
	path('manufacturer/<str:cpu_slug>/', ManufacturerView.as_view(), name='show_manufacturer'),
	path('<str:slug>/', GoodView.as_view(), name='show_good'),
]

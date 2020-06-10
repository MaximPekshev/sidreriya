from django.contrib import admin
from .models import Cart
from .models import Cart_Item


class Cart_ItemInline(admin.TabularInline):
    model = Cart_Item
    extra = 0

class CartAdmin(admin.ModelAdmin):
	list_display = (
					'user',
					'summ', 
					)
	
	inlines 	 = [Cart_ItemInline]

admin.site.register(Cart, CartAdmin)
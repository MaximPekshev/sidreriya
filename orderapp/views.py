from django.shortcuts import render
from .models import Order, Order_Item
from authapp.models import Buyer
from cartapp.views import get_cart
from cartapp.models import Cart, Cart_Item
import django.core.exceptions
from authapp.forms import BuyerSaveForm
from goodapp.views import get_in_barrels

def show_orders(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
		'in_bar': get_in_barrels(),

	}

	try:

		orders_full = []

		buyer = Buyer.objects.get(user=request.user)
		orders = Order.objects.filter(buyer=buyer).order_by("-date")
		for order in orders:
			qty = 0
			order_items = Order_Item.objects.filter(order=order)
			for n in order_items:
				qty += n.quantity

			orders_full.append([order, qty])

			context.update({

				'orders': orders_full

				})

		return render(request, 'orderapp/orders.html', context)

	except Buyer.DoesNotExist:

		return render(request, 'orderapp/orders.html', context)


def order_add(request):

	if request.method == 'POST':

		buyer_form = BuyerSaveForm(request.POST)

		if buyer_form.is_valid():

			first_name 	= buyer_form.cleaned_data['input_first_name']
			last_name	= buyer_form.cleaned_data['input_second_name']
			phone 		= buyer_form.cleaned_data['input_phone']
			locality  	= buyer_form.cleaned_data['input_locality']
			street  	= buyer_form.cleaned_data['input_street']
			house  		= buyer_form.cleaned_data['input_house']
			apartments  = buyer_form.cleaned_data['input_apartments']
			porch  		= buyer_form.cleaned_data['input_porch']
			floor 		= buyer_form.cleaned_data['input_floor']

	
			try:

				if request.user.is_authenticated:
				
					buyer = Buyer.objects.get(user = request.user)

				else:
					
					buyer = None	

			except Buyer.DoesNotExist:
				
				buyer = Buyer(
				user = request.user,
				first_name = first_name,
				last_name = last_name, 
				phone = phone,
				locality = locality,
				street = street, 
				house = house,
				apartments = apartments,
				porch = porch,
				floor = floor,

				)

				buyer.save()

			if buyer:

				new_order = Order(
					first_name=first_name, 
					last_name=last_name, 
					phone=phone, 
					buyer=buyer, 
					address = "{}, {} ул., д. {}, кв. {}, подъезд {}, этаж {}".format(locality, street, house, apartments, porch, floor))
			else:

				new_order = Order(
					first_name=first_name, 
					last_name=last_name, 
					phone=phone, 
					address = "{}, {} ул., д. {}, кв. {}, подъезд {}, этаж {}".format(locality, street, house, apartments, porch, floor))

			new_order.save()
			
			cart_items = Cart_Item.objects.filter(cart=get_cart(request))

			for item in cart_items:

				order_item = Order_Item(

					order = new_order,
					good = item.good,
					quantity = item.quantity,
					price = item.price,
					summ = item.summ,

					)
				order_item.save()

			cart_to_clear = get_cart(request)

			cart_items_to_delete = Cart_Item.objects.filter(cart=cart_to_clear)

			for item in cart_items_to_delete:

				item.delete()

			cart_to_clear.summ = 0	
			cart_to_clear.save()	

			context = {

				'order': new_order, 'order_items': Order_Item.objects.filter(order=new_order),
				'cart': get_cart(request),
				'cart_count' : len(Cart_Item.objects.filter(cart=get_cart(request))),
				'in_bar': get_in_barrels(),

				}



			return render(request, 'orderapp/order_created.html', context)
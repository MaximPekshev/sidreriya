from django.shortcuts import render
from .models import Order, Order_Item
from authapp.models import Buyer
from cartapp.views import get_cart
from cartapp.models import Cart, Cart_Item
from goodapp.models import Good
import django.core.exceptions
from authapp.forms import BuyerSaveForm
from goodapp.views import get_in_barrels
import datetime

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.db.models import Sum

from wishlistapp.views import get_wishlist
from wishlistapp.models import Wishlist, Wishlist_Item

from decouple import config

from decimal import Decimal

from .tasks import cel_send_mail_on_bar, cel_send_mail_to_buyer


# helpers


# views

def show_orders(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

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

			first_name 		= buyer_form.cleaned_data['input_first_name']
			last_name		= buyer_form.cleaned_data['input_second_name']
			phone 			= buyer_form.cleaned_data['input_phone']
			locality  		= buyer_form.cleaned_data['input_locality']
			street  		= buyer_form.cleaned_data['input_street']
			house  			= buyer_form.cleaned_data['input_house']
			apartments  	= buyer_form.cleaned_data['input_apartments']
			porch  			= buyer_form.cleaned_data['input_porch']
			floor 			= buyer_form.cleaned_data['input_floor']
			input_cook_time = buyer_form.cleaned_data['input_cook_time']
			input_time 		= buyer_form.cleaned_data['input_time']
			input_email 	= buyer_form.cleaned_data['input_email']
			quantity 		= buyer_form.cleaned_data['quantity']
			comment 		= buyer_form.cleaned_data['comment']

			if street:
				address =  "{}, {} ул., д. {}, кв. {}, подъезд {}, этаж {}".format(locality, street, house, apartments, porch, floor)
			else:
				address = "Самовывоз - ул. Костюкова 36Г, Белгород"

	
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
				email = input_email,
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
					email = input_email,
					address = address,
					cook_time= "{}".format(str(input_time) if input_cook_time=="by_time" else "Как можно скорее"),
					comment=comment,
						)

			else:

				new_order = Order(
					first_name=first_name, 
					last_name=last_name, 
					phone=phone, 
					address = address,
					email = input_email,
					cook_time= "{}".format(str(input_time) if input_cook_time=="by_time" else "Как можно скорее"),
					comment=comment,
					)

			new_order.save()

			if quantity:

				set_lunch_good = Good.objects.filter(name="Комплексный обед").first()

				order_item = Order_Item(

					order = new_order,
					good = set_lunch_good,
					quantity = Decimal(quantity),
					price = set_lunch_good.price,
					summ = set_lunch_good.price*Decimal(quantity),

					)
				order_item.save()


			else:	
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
				
				cel_send_mail_to_buyer.delay(new_order.pk, input_email)
		        
			cel_send_mail_on_bar.delay(new_order.pk)

			context = {

				'order': new_order, 'order_items': Order_Item.objects.filter(order=new_order),
				'cart': get_cart(request),
				'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
				'in_bar': get_in_barrels(),
				'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 

				}

			return render(request, 'orderapp/order_created.html', context)

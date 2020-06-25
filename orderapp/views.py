from django.shortcuts import render
from .models import Order, Order_Item
from authapp.models import Buyer
from cartapp.views import get_cart
from cartapp.models import Cart, Cart_Item
import django.core.exceptions
from authapp.forms import BuyerSaveForm
from goodapp.views import get_in_barrels
import datetime

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.db.models import Sum

def show_orders(request):

	context = {

		'cart': get_cart(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
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
						)

			else:

				new_order = Order(
					first_name=first_name, 
					last_name=last_name, 
					phone=phone, 
					address = address,
					email = input_email,
					cook_time= "{}".format(str(input_time) if input_cook_time=="by_time" else "Как можно скорее"),
					)

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

			send_mail_to_buyer(new_order, input_email)
			send_mail_on_bar(new_order)

			context = {

				'order': new_order, 'order_items': Order_Item.objects.filter(order=new_order),
				'cart': get_cart(request),
				'cart_count' : Cart_Item.objects.filter(cart=get_cart(request)).aggregate(Sum('quantity'))['quantity__sum'],
				'in_bar': get_in_barrels(),

				}



			return render(request, 'orderapp/order_created.html', context)



def send_mail_to_buyer(order, buyer_email):

	HOST = "mail.hosting.reg.ru"
	sender_email = "info@sidreriyabelgorod.ru"
	receiver_email = [ buyer_email ]
	password = "3X3w5I7g"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Заказ № {} от {}, Сидрерия".format(order.order_number, order.date.strftime("%Y-%m-%d")) 
	message["From"] = sender_email
	message["To"] = ','.join(receiver_email)

	order_items = ""

	css_style_td = """\
	style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: center;"
	"""

	if order:
		for item in Order_Item.objects.filter(order=order):
			order_items += "<tr><td {3}>{0}</td> <td {3}>x{1}</td> <td{3}>{2}</td></tr>".format(item.good, item.quantity, item.summ, css_style_td)



		text = """\
		{}""".format(order_items)


		html = """\
	    <html>
	      <body>
	      <div style="max-width: 610px; width:100%">
	        <H4 style="background-color: #262626; color: #fff; padding: 12px 0; text-align: center; font-size: 14px; margin-bottom: 30px;">Заказ принят</H4>
	        <H4>Здравствуйте, {0}</H4>
	        <p>Мы получили Ваш заказ.В ближайшее время наши бармены с Вами свяжутся для уточнения деталей</p>
	        <p>Номер заказа: {1}</p>
	        <p>Адрес доставки: {2}</p>
	        <p>Время приготовления: {3}</p>
	        
			<table style="max-width:600px; width:100%; margin:0; padding:0;" border="0" cellpadding="0">
				<thead>
					<tr>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: left">Товар</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Кол-во</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Сумма</th>
					</tr>
				</thead>
				<tbody>
					{4}
				</tbody>
				<tfoot>
					<tr >
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<th style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;">Итого</th>
						<td style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;"><strong><span>&#8381 {5}</span></strong></td>
					</tr>
				</tfoot>
			</table>	

	        <p></p>

	        <p>
				Стоимость вашего заказа указана без скидок!
			</p>
			<p>	
				На данный момент действуют акции:<br> -25% на весь сидр «с собой»<br> -20% на основное меню при самовывозе<br>
			</p>
			<p>
				Скидка будет примена по факту подтверждения заказа нашими барменами.
			</p>
			<p>
				<a href="http://sidreriyabelgorod.ru/delivery/" target="_blank"> О нашей доставке </a>
			</p>
			<p></p>
			<p> С Уважением, Сидрерия </p>
			</div>
	      </body>
	    </html>
	    """.format(order.first_name, order.order_number, order.address, order.cook_time, order_items, order.summ)

	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	message.attach(part1)
	message.attach(part2)
	context = ssl.create_default_context()
	server = smtplib.SMTP(HOST, 587)
	server.starttls()
	server.login(sender_email, password)
	server.sendmail(
	sender_email, receiver_email , message.as_string()
	)
	server.quit()

def send_mail_on_bar(order):

	HOST = "mail.hosting.reg.ru"
	sender_email = "info@sidreriyabelgorod.ru"
	receiver_email = ['info@sidreriyabelgorod.ru']
	password = "3X3w5I7g"

	message = MIMEMultipart("alternative")
	message["Subject"] = "Поступил заказ № {} от {}".format(order.order_number, order.date.strftime("%Y-%m-%d")) 
	message["From"] = sender_email
	message["To"] = ','.join(receiver_email)

	order_items = ""

	css_style_td = """\
	style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: center;"
	"""

	if order:
		for item in Order_Item.objects.filter(order=order):
			order_items += "<tr><td {3}>{0}</td> <td {3}>x{1}</td> <td{3}>{2}</td></tr>".format(item.good, item.quantity, item.summ, css_style_td)



		text = """\
		{}""".format(order_items)


		html = """\
	    <html>
	      <body>
	      <div style="max-width: 610px; width:100%">
	        <H4 style="background-color: #262626; color: #fff; padding: 12px 0; text-align: center; font-size: 14px; margin-bottom: 30px;">Поступил Заказ</H4>
	        <p>Номер заказа: {0}</p>
	        <p>Клиент: {6} {7}</p>
	        <p>Номер телефона: {1}</p>
	        <p>Email: {8}</p>
	        <p>Адрес доставки: {2}</p>
	        <p>Время приготовления: {3}</p>
	        
			<table style="max-width:600px; width:100%; margin:0; padding:0;" border="0" cellpadding="0">
				<thead>
					<tr>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: left">Товар</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Кол-во</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Сумма</th>
					</tr>
				</thead>
				<tbody>
					{4}
				</tbody>
				<tfoot>
					<tr >
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<th style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;">Итого</th>
						<td style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;"><strong><span>&#8381 {5}</span></strong></td>
					</tr>
				</tfoot>
			</table>	

	        <p></p>
			</div>
	      </body>
	    </html>
	    """.format(order.order_number, order.phone, order.address, order.cook_time, order_items, order.summ, order.first_name, order.last_name, order.email)

	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	message.attach(part1)
	message.attach(part2)
	context = ssl.create_default_context()
	server = smtplib.SMTP(HOST, 587)
	server.starttls()
	server.login(sender_email, password)
	server.sendmail(
	sender_email, receiver_email , message.as_string()
	)
	server.quit()
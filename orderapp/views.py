from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decimal import Decimal
from decouple import config
import time

from .models import Order, Order_Item
from .forms import OrderCreateForm
from authapp.models import Buyer
from authapp.forms import BuyerSaveForm
from cartapp.services import cart_object
from cartapp.models import Cart_Item
from cartapp.models import cart_calculate_summ
from goodapp.models import Good

# helpers
def send_mail_on_bar(order_id):
	try:
		order = Order.objects.get(pk=order_id)
	except:
		order = None	
	HOST = "mail.hosting.reg.ru"
	sender_email = config('MAIL_USER')
	receiver_email = ['info@sidreriyabelgorod.ru', 'alena-go@bk.ru', 'sidreriya.bel@gmail.com']
	# receiver_email = ['m.pekshev@annasoft.ru',]
	password = config('MAIL_PASSWORD')
	message = MIMEMultipart("alternative")
	message["Subject"] = "Поступил заказ № {} от {}".format(order.order_number, order.date.strftime("%d-%m-%Y")) 
	message["From"] = sender_email
	message["To"] = ','.join(receiver_email)
	order_items = ""
	css_style_td = """\
	style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: center;"
	"""
	if order:
		for item in Order_Item.objects.filter(order=order):
			order_items += "<tr><td {3}>{0}</td> <td {3}>x{1}</td> <td{3}>{2}</td> <td{3}>{4}</td></tr>".format(item.good, item.quantity, item.summ, css_style_td, item.discount_summ())
		text = """\
		{}""".format(order_items)
		html = """\
	    <html>
	      <body>
	      <div style="max-width: 610px; width:100%">
	        <H4 style="background-color: #262626; color: #fff; padding: 12px 0; text-align: center; font-size: 14px; margin-bottom: 30px;">Поступил Заказ</H4>
	        <p>Номер заказа: # {0}</p>
	        <p>Клиент: {6} {7}</p>
	        <p>Номер телефона: {1}</p>
	        <p>Email: {8}</p>
	        <p>Адрес доставки: {2}</p>
	        <p>Время приготовления: {3}</p>
	        <p></p>
	        <p>Комментарий покупателя:<br> {9}</p>
	        
			<table style="max-width:600px; width:100%; margin:0; padding:0;" border="0" cellpadding="0">
				<thead>
					<tr>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: left">Товар</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Кол-во</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Сумма</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">С собой</th>
					</tr>
				</thead>
				<tbody>
					{4}
				</tbody>
				<tfoot>
					<tr >
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<th style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;">Итого</th>
						<td style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;"><strong><span>&#8381 {5}</span></strong></td>
					</tr>
					<tr >
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<th style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;">С собой</th>
						<td style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;"><strong><span>&#8381 {10}</span></strong></td>
					</tr>
				</tfoot>
			</table>	

	        <p></p>
			</div>
	      </body>
	    </html>
	    """.format(order.order_number, order.phone, order.address, order.cook_time, order_items, order.summ, order.first_name, order.last_name, order.email, order.comment, order.discount_summ())

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


def send_mail_to_buyer(order_id, buyer_email):
	try:
		order = Order.objects.get(id=order_id)
	except:
		order = None
	HOST = "mail.hosting.reg.ru"
	sender_email = config('MAIL_USER')
	receiver_email = [ buyer_email ]
	password = config('MAIL_PASSWORD')
	message = MIMEMultipart("alternative")
	message["Subject"] = "Заказ № {} от {}, Сидрерия".format(order.order_number, order.date.strftime("%d-%m-%Y")) 
	message["From"] = sender_email
	message["To"] = ','.join(receiver_email)
	order_items = ""
	css_style_td = """\
	style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: center;"
	"""
	if order:
		for item in Order_Item.objects.filter(order=order):
			order_items += "<tr><td {3}>{0}</td> <td {3}>x{1}</td> <td{3}>{2}</td> <td{3}>{4}</td></tr>".format(item.good, item.quantity, item.summ, css_style_td, item.discount_summ())
		text = """\
		{}""".format(order_items)
		html = """\
	    <html>
	      <body>
	      <div style="max-width: 610px; width:100%">
	        <H4 style="background-color: #262626; color: #fff; padding: 12px 0; text-align: center; font-size: 14px; margin-bottom: 30px;">Заказ принят</H4>
	        <H4>Здравствуйте, {0}</H4>
	        <p>Мы получили Ваш заказ.В ближайшее время наши бармены с Вами свяжутся для уточнения деталей</p>
	        <p>Номер заказа: # {1}</p>
	        <p>Адрес доставки: {2}</p>
	        <p>Время приготовления: {3}</p>
	        
			<table style="max-width:600px; width:100%; margin:0; padding:0;" border="0" cellpadding="0">
				<thead>
					<tr>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0; text-align: left">Товар</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Кол-во</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">Сумма</th>
						<th style="border-bottom: 1px solid #ececec; padding: 14px 0;">С собой</th>
					</tr>
				</thead>
				<tbody>
					{4}
				</tbody>
				<tfoot>
					<tr >
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<th style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;">Итого</th>
						<td style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;"><strong><span>&#8381 {5}</span></strong></td>
					</tr>
					<tr >
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<td style="border-bottom: 1px solid #ececec; padding: 14px 0;"></td>
						<th style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;">С собой</th>
						<td style="text-align: center; border-bottom: 1px solid #ececec; padding: 14px 0;"><strong><span>&#8381 {6}</span></strong></td>
					</tr>
				</tfoot>
			</table>	

	        <p></p>

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

			<p>	
				Костюкова:<br>
				Вс-Чт : 9-00/0-00<br> 
				Пт-Сб : 9-00/2-00
			</p>
			<p>	
				Левобережная:<br>
				Пн-Чт : 11-00/0-00<br> 
				Пт : 11-00/2-00<br>
				Сб : 14-00/2-00<br>
				Вс : 14-00/0-00<br>
			</p>
			</div>
	      </body>
	    </html>
	    """.format(order.first_name, order.order_number, order.address, order.cook_time, order_items, order.summ, order.discount_summ())

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

# views
def show_orders(request):

	context = {
		
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

# функция создает строки Заказа
# def create_order_item(order, order_item_slug, qty, summ):
# 	try:
# 		good = Good.objects.get(slug = order_item_slug)
# 		order_item = Order_Item(
# 			order = order,
# 			good = good,
# 			quantity = Decimal(qty),
# 			price = Decimal(summ)/Decimal(qty),
# 			summ = Decimal(summ),
# 			)
# 		order_item.save()
# 		return order_item
# 	except:
# 		return None

# новая функция создания заказа с фронта
@transaction.atomic
def order_create(request, *args, **kwargs):
	if request.method == 'POST':
		order_form = OrderCreateForm(request.POST)
		if order_form.is_valid():
			# orderType = 1 - Доставка, = 2 - Самовывоз
			order_type = order_form.cleaned_data['orderType']
			input_qty = order_form.cleaned_data['input_qty']
			input_name = order_form.cleaned_data['input_name']
			input_last_name = order_form.cleaned_data['input_last_name']
			input_phone = order_form.cleaned_data['input_phone']
			input_comment = order_form.cleaned_data['input_comment']
			input_email = order_form.cleaned_data['input_email']

			new_order = Order(
				first_name = input_name,
				phone = input_phone,
				comment = input_comment,
			)

			# slug товара, если товар 1 (обеды или фестивальные позиции)
			good_slug = order_form.cleaned_data['good_slug']
			# список товаров, если заказ производится из Корзины
			order_items_list = order_form.cleaned_data['order_items_list']
			# cookTimeType = 1 - Как можно скорее, = 2 - Выбрать время
			cook_time_type = order_form.cleaned_data['cookTimeType']
			# если приготовление ко времени, получаем время приготовления
			if cook_time_type == '2':
				input_time = order_form.cleaned_data['inputTime']
				new_order.cook_time = str(input_time)
			elif cook_time_type == '1':
				new_order.cook_time = "Как можно скорее"
			# если тип заказа Доставка - получаем адрес доставки
			if order_type == '1':
				input_address = order_form.cleaned_data['input_address']
				new_order.address = input_address
			# если тип заказа Самовывоз - получаем место самовывоза
			# pickup_type = 1 - Сидрерии на Везелке, pickup_type = 2 - Сидрерии на Костюкова.
			elif order_type == '2':
				pickup_type = order_form.cleaned_data['pickupType']
				if pickup_type == '1':
					new_order.address = "Самовывоз - ул. Левобережная 22А, Белгород"
				elif pickup_type == '2':
					new_order.address = "Самовывоз - ул. Костюкова 36Г, Белгород"	
			# если пользователь авторизован - добавляем в заказ созданного покупателя.	
			if request.user.is_authenticated:
				try:
					buyer = Buyer.objects.get(user = request.user)
				except Buyer.DoesNotExist:
					buyer = Buyer.objects.create(
						user = request.user,
						first_name = input_name,
						phone = input_phone,
						)
					if input_last_name:
						buyer.last_name = input_last_name
					buyer.save()	
				new_order.buyer = buyer
			new_order.save()
			# если в форме передается идентификатор одного Товара, то добавляем в заказ только этот товар.
			if good_slug:
				try:
					good = Good.objects.get(slug = good_slug)
					order_item = Order_Item(
						order = new_order,
						good = good,
						quantity = Decimal(input_qty),
						price = good.price,
						summ = good.price*Decimal(input_qty),
						)
					order_item.save()
				except:
					return JsonResponse(
						data={'error': 'Не удалось создать заказ!!'},
						status=400
					)
			# если на входе получаем список из товаров в заказе, то добавляем товары в цикле
			elif order_items_list:
				order_items_list = json.loads(order_items_list)
				for order_item in order_items_list:
					order_item_slug = order_item
					order_item =  order_items_list.get(order_item)
					qty = order_item.get("qty")
					summ = order_item.get("summ")
					good = Good.objects.filter(slug=order_item_slug).first()
					order_item = Order_Item(
						order = new_order,
						good = good,
						quantity = Decimal(qty),
						price = Decimal(summ)/Decimal(qty),
						summ = Decimal(summ),
						)
					order_item.save()
					# create_order_item(new_order, order_item_slug, order_item.get("qty"), order_item.get("summ"))
				# удаляем из корзины товар, который успешно попал в заказ
				cart = cart_object(request)
				cart_items = Cart_Item.objects.filter(cart=cart)
				for order_item in order_items_list:
					order_item_slug = order_item
					order_item =  order_items_list.get(order_item)
					try:
						cart_item = cart_items.get(good__slug=order_item_slug)
						if cart_item.quantity <= Decimal(order_item.get("qty")):
							cart_item.delete()
						else:
							cart_item.quantity -= Decimal(order_item.get("qty"))
							cart_item.save()
					except:
						pass
					cart_calculate_summ(cart)
			elif len(order_items_list) == 0:
				new_order.delete()
				return JsonResponse(
					data={
						'error': 'Не удалось создать заказ!! Попробуйте позже.',
					},
					status=400
				)

			new_order_items = Order_Item.objects.filter(order=new_order)
			if new_order_items:
				#если указан email отправляем данные по заказу Покупателю
				if input_email:
					send_mail_to_buyer(new_order.id, input_email)
				# отправляем заказ для обработки сотрудниками.	
				send_mail_on_bar(new_order.id)
				return JsonResponse(
					data={
						'data': 'Заказ {} от {} успешно создан!'.format(new_order.order_number, new_order.date.strftime("%d-%m-%y %H:%m")),
						'message': 'В ближайшее время с Вами свяжется наш сотрудник для уточнения деталей.'
					},
					status=200
					)
			else:
				new_order.delete()
				return JsonResponse(
					data={
						'error': 'Не удалось создать заказ!! Попробуйте позже.',
					},
					status=400
				)
			
	return JsonResponse(
		data={'error': 'Не удалось создать заказ!!'},
		status=400
	)

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
			good_id 		= buyer_form.cleaned_data['good_id']
			input_location 	= buyer_form.cleaned_data['input_location']

			if street:
				address =  "{}, {} ул., д. {}, кв. {}, подъезд {}, этаж {}".format(locality, street, house, apartments, porch, floor)
			else:
				if input_location == '1':

					address = "Самовывоз - ул. Костюкова 36Г, Белгород"

				elif input_location == '2':

					address = "Самовывоз - ул. Левобережная 22А, Белгород"

	
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

			if good_id == 'lunch' :

				set_lunch_good = Good.objects.filter(name="Дружеский обед").first()

				order_item = Order_Item(

					order = new_order,
					good = set_lunch_good,
					quantity = Decimal(quantity),
					price = set_lunch_good.price,
					summ = set_lunch_good.price*Decimal(quantity),

					)
				order_item.save()

			elif good_id == 'gift' :

				gift_good = Good.objects.filter(name="Подарочная коробка").first()

				order_item = Order_Item(

					order = new_order,
					good = gift_good,
					quantity = Decimal(quantity),
					price = gift_good.price,
					summ = gift_good.price*Decimal(quantity),

					)
				order_item.save()


			else:	
				cart_items = Cart_Item.objects.filter(cart=cart_object(request))

				for item in cart_items:
					if item.good.quantity !=0:
						order_item = Order_Item(

							order = new_order,
							good = item.good,
							quantity = item.quantity,
							price = item.price,
							summ = item.summ,

							)
						order_item.save()

				cart_to_clear = cart_object(request)

				cart_items_to_delete = Cart_Item.objects.filter(cart=cart_to_clear)

				for item in cart_items_to_delete:

					item.delete()

				cart_to_clear.summ = 0
				cart_to_clear.save()
				
				send_mail_to_buyer(new_order.id, input_email)

			send_mail_on_bar(new_order.id)

			context = {
				'order': new_order, 'order_items': Order_Item.objects.filter(order=new_order),
			}

			return render(request, 'orderapp/order_created.html', context)

from rest_framework.views import APIView
import logging
from .serializers import SimpleOrderSerializer
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def clear_cart(request):
	cart = cart_object(request)
	cart_items = Cart_Item.objects.filter(cart=cart)
	for item in cart_items:
		item.delete()
	cart.summ = 0
	cart.save()

# Вспомогательная функция для получения объекта Good по его slug (good_id)
def good_by_id(good_id):
	return Good.objects.filter(slug=good_id).first()

def handle_items_order(items_list, order):
	# Проходим по каждому товару в списке товаров заказа
	for item_dir in items_list:
		# Создаем объект Order_Item для текущего заказа
		item_order = Order_Item(order=order)
		# Получаем товар по good_id, если он есть
		key_name = "good_id"
		if key_name in item_dir:
			good_id = item_dir.get(key_name)
			item_order.good = None if good_id is None else good_by_id(good_id=good_id)
		# Устанавливаем количество товара, если указано
		key_name = "quantity"
		if key_name in item_dir:
			setattr(item_order, key_name, item_dir.get(key_name))
		# Устанавливаем цену товара, если указано
		key_name = "price"
		if key_name in item_dir:
			setattr(item_order, key_name, item_dir.get(key_name))
		# Устанавливаем сумму по товару, если указано
		key_name = "summ"
		if key_name in item_dir:
			setattr(item_order, key_name, item_dir.get(key_name))
		# Сохраняем объект Order_Item в базе данных
		item_order.save()

def handle_order(order, user):
	with transaction.atomic():
		# Создаем новый объект заказа
		orderObject = Order.objects.create()
		# Если пользователь авторизован — ищем или создаем покупателя
		if user.is_authenticated:
			try:
				buyer = Buyer.objects.get(user=user)
			except Buyer.DoesNotExist:
				buyer = Buyer.objects.create(
					user = user,
					first_name = order.first_name,
					phone = order.phone,
					)
				buyer.save()	
			orderObject.buyer = buyer
		# Получаем список товаров из заказа и добавляем их к заказу
		items = order.get("items")
		handle_items_order(items, order=orderObject)
		# Заполняем основные поля заказа
		orderObject.first_name = order.get("first_name")
		orderObject.phone = order.get("phone")
		# Обработка времени приготовления
		cookTimeType = order.get("cookTimeType")
		if cookTimeType == "1":
			orderObject.cook_time = "Как можно скорее"
		elif cookTimeType == "2":
			orderObject.cook_time = order.get("cookTime")
		# Обработка типа заказа (доставка или самовывоз)
		orderType = order.get("orderType")
		if orderType == "1":
			orderObject.address = order.get("address")
		elif orderType == "2":
			pickupType = order.get("pickupType")
			if pickupType == "1":
				orderObject.address = "Самовывоз - ул. Костюкова 36Г, Белгород"
			elif pickupType == "2":
				orderObject.address = "Самовывоз - ул. Левобережная 22А, Белгород"
		# Сохраняем заказ
		orderObject.save()
		return orderObject

class OrderView(APIView):
	# Обработка POST-запроса для создания заказа
	def post(self, request):
		response = {"data": []}
		# Получаем данные заказа из запроса
		data = request.data.get("data")
		if not data:
			# Если данных нет — возвращаем пустой ответ
			return Response(response)
		logger.info({"order_data": data})
		# Сериализуем данные заказа для валидации
		serializer = SimpleOrderSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			# Если данные валидны — создаём заказ
			order = handle_order(order=data, user=request.user)
			# Если указан email — отправляем письмо покупателю
			if order.email:
				send_mail_to_buyer(order.id, order.email)
			# Отправляем письмо сотрудникам бара
			send_mail_on_bar(order.id)
			# Очищаем корзину пользователя
			try:
				clear_cart(request)
			except:
				pass	
			return JsonResponse(
				data={
					'data': 'Заказ {} от {} успешно создан!'.format(order.order_number, order.date.strftime("%d-%m-%Y")),
					'message': 'В ближайшее время с Вами свяжется наш сотрудник для уточнения деталей.'
				},
				status=200
			)
		else:
			# Если данные невалидны — логируем ошибку и возвращаем ошибку клиенту
			logger.error({"order_error": serializer.errors})
			response["error"] = "Ошибка валидации данных заказа"
			return JsonResponse(data=response, status=400)
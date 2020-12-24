
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

from background_task import background


@background(schedule=2)
def sand_mail_to_me():

	HOST = "mail.hosting.reg.ru"
	sender_email = config('MAIL_USER')
	receiver_email = ['m.pekshev@annasoft.ru',]
	password = config('MAIL_PASSWORD')

	message = MIMEMultipart("alternative")
	message["Subject"] = "Тестовое сообщение"
	message["From"] = sender_email
	message["To"] = ','.join(receiver_email)

	
	text = """\
	Тестовое сообщение"""


	html = """\
    <html>
      <body>
      <div style="max-width: 610px; width:100%">
        <H4 style="background-color: #262626; color: #fff; padding: 12px 0; text-align: center; font-size: 14px; margin-bottom: 30px;">Сообщение отправлено!</H4>
        <p></p>
		</div>
      </body>
    </html>
    """

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

@background(schedule=1)
def send_mail_on_bar(order_id):

	try:
		order = Order.objects.get(pk=order_id)
	except:
		order = None	
			
	HOST = "mail.hosting.reg.ru"
	sender_email = config('MAIL_USER')
	# receiver_email = ['info@sidreriyabelgorod.ru', 'alena-go@bk.ru', 'sidreriya.bel@gmail.com']
	receiver_email = ['m.pekshev@annasoft.ru',]
	password = config('MAIL_PASSWORD')

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
	        <p></p>
	        <p>Комментарий покупателя:<br> {9}</p>
	        
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
	    """.format(order.order_number, order.phone, order.address, order.cook_time, order_items, order.summ, order.first_name, order.last_name, order.email, order.comment)

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


@background(schedule=1)
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
			<p>	
				Часы работы:<br> Пн-Чт : 11:00/0:00<br>Пт : 11-00/3-00<br>Сб : 14-00/3-00<br>Вс : 14-00/0-00
			</p>
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
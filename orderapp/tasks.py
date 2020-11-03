from sidreriya.celery import app

from .service import send_mail_on_bar, send_mail_to_buyer
from .models import Order



@app.task
def cel_send_mail_on_bar(order_pk):

	order = Order.objects.get(pk=order_pk)
	send_mail_on_bar(order)

@app.task
def cel_send_mail_to_buyer(order_pk, email):

	order = Order.objects.get(pk=order_pk)
	send_mail_to_buyer(order, email)
from django.db import models

from django.conf import settings

from goodapp.models import Good
from authapp.models import Buyer


class Order(models.Model):
	summ		= models.DecimalField('Сумма заказа', default = 0, blank = True, max_digits = 15, decimal_places = 0, editable = False)
	buyer 		= models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)	
	order_number= models.CharField(max_length=10, verbose_name='Номер заказа')

	date 		= models.DateTimeField('Дата заказа', auto_now_add = True)

	address 	= models.CharField(max_length=1024, verbose_name='Адрес', blank=True)

	cook_time 	= models.CharField(max_length=20, verbose_name='Время приготовления', blank=True)

	first_name 	= models.CharField(max_length=150, verbose_name='Имя', blank=True)
	last_name 	= models.CharField(max_length=150, verbose_name='Фамилия', blank=True)
	phone	 	= models.CharField(max_length=150, verbose_name='Телефон', blank=True, null=True)
	email 		= models.CharField(max_length=30, verbose_name='Email', blank=True)

	def __str__(self):
		return str(self.id)

	def save(self, *args,  **kwargs):

		self.summ = 0

		or_it = Order_Item.objects.filter(order=self)
		for item in or_it:

			self.summ += item.summ

		if self.order_number:
			pass
		else:	
			self.order_number = str(len(Order.objects.all()) + 1)	

		super(Order, self).save(*args, **kwargs)	

	class Meta:
		
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

class Order_Item(models.Model):

	order 		= models.ForeignKey(Order, on_delete = models.CASCADE)
	good 		= models.ForeignKey(Good, on_delete = models.PROTECT)
	quantity	= models.DecimalField(max_digits = 15, decimal_places = 1)
	price		= models.DecimalField(max_digits = 15, decimal_places = 0)
	summ		= models.DecimalField(max_digits = 15, decimal_places = 0)


	def __str__(self):
		return str(self.id)

	def save(self, *args,  **kwargs):

		self.summ = self.price * self.quantity

		super(Order_Item, self).save(*args, **kwargs)
		self.order.save()
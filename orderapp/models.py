from django.db import models

from decimal import Decimal

from goodapp.models import Good
from authapp.models import Buyer


class Order_Item(models.Model):
	order 		= models.ForeignKey('Order', on_delete = models.CASCADE)
	good 		= models.ForeignKey(Good, on_delete = models.PROTECT)
	quantity	= models.DecimalField(max_digits = 15, decimal_places = 1)
	price		= models.DecimalField(max_digits = 15, decimal_places = 0)
	summ		= models.DecimalField(max_digits = 15, decimal_places = 0)
	def __str__(self):
		return str(self.id)

	def save(self, *args,  **kwargs):
		self.summ = Decimal(self.price) * Decimal(self.quantity)
		super(Order_Item, self).save(*args, **kwargs)
		self.order.save()

	def discount_price(self):
		if self.good.is_cidre:	
			s = self.price - self.price*Decimal(0.25)
		else:
			if self.good.category.name == "Сертификаты" or self.good.name == 'Дружеский обед' or self.good.category.name == "Куличи" or self.good.category.name == "Вареники":
				s = self.price
			else:
				s = self.price - self.price*Decimal(0.2)
		return s.quantize(Decimal("1"))

	def discount_summ(self):
		s = self.quantity*self.discount_price()
		return s.quantize(Decimal("1"))	

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
	comment 	= models.TextField(verbose_name='Комментарий', blank=True)

	def __str__(self):
		return str(self.order_number)

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

	def discount_summ(self):
		summ = Decimal(0)
		for item in Order_Item.objects.filter(order=self):
			summ += item.quantity*item.discount_price()
		return summ.quantize(Decimal("1"))
	
	def order_type(self):
		order_items = Order_Item.objects.filter(order=self)
		if len(order_items) == 1 and order_items[0].good.name == "Дружеский обед":
			return "Обед"
		else:
			return "Заказ"	
	
	class Meta:
		
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'
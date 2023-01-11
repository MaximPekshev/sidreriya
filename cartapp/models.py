from django.db import models

from django.conf import settings

from goodapp.models import Good
from decimal import Decimal

def cart_calculate_summ(cart):

	if cart:
		cart_items = Cart_Item.objects.filter(cart=cart)

		summ_of_cart = 0

		for item in cart_items:
			summ_of_cart += item.summ

		cart.summ = summ_of_cart
		cart.save()


class Cart_Item(models.Model):

	cart 		= models.ForeignKey('Cart', on_delete = models.CASCADE)
	good 		= models.ForeignKey(Good, on_delete = models.PROTECT)
	quantity	= models.DecimalField(max_digits = 15, decimal_places = 1)
	price		= models.DecimalField(max_digits = 15, decimal_places = 0)
	summ		= models.DecimalField(max_digits = 15, decimal_places = 0)

	def __str__(self):
		return str(self.id)

	def save(self, *args, **kwargs):
		self.price = self.price if self.price else 0
		self.summ = self.price * self.quantity
		super(Cart_Item, self).save(*args, **kwargs)
		cart_calculate_summ(self.cart)	

	def get_discount_price(self):

		if self.good.is_cidre:	
			s = self.price - self.price*Decimal(0.25)
		else:
			if self.good.category.name == "Сертификаты" or self.good.name == 'Дружеский обед' or self.good.category.name == "Куличи" or self.good.category.name == "Вареники":
				s = self.price
			else:
				s = self.price - self.price*Decimal(0.2)

		return s.quantize(Decimal("1"))

	def get_item_discount_summ(self):
		s = self.quantity*self.get_discount_price()
		return s.quantize(Decimal("1"))

class Cart(models.Model):

	summ		= models.DecimalField('Сумма корзины', default = 0, blank = True, max_digits = 15, decimal_places = 0, editable = False)
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)		

	def get_discount_summ(self):
		summ = Decimal(0)
		for item in Cart_Item.objects.filter(cart=self):
			summ += item.quantity*item.get_discount_price()
		return summ.quantize(Decimal("1"))

	def __str__(self):
		return str(self.id)
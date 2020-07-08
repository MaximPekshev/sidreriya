from django.db import models

from django.conf import settings

from goodapp.models import Good


def cart_calculate_summ(cart):

	if cart:
		cart_items = Cart_Item.objects.filter(cart=cart)

		summ_of_cart = 0

		for item in cart_items:
			summ_of_cart += item.summ

		cart.summ = summ_of_cart
		cart.save()


class Cart(models.Model):

	summ		= models.DecimalField('Сумма корзины', default = 0, blank = True, max_digits = 15, decimal_places = 0, editable = False)
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)		

	def __str__(self):
		return str(self.id)

class Cart_Item(models.Model):

	cart 		= models.ForeignKey(Cart, on_delete = models.CASCADE)
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


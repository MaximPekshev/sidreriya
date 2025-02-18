from django.shortcuts import render
from django.views.generic import View
import datetime

from goodapp.models import (
	Category, 
	Set_Lunch, 
	Good,
	Bestseller
)
from baseapp.models import (
	Breakfast 
)
from festapp.models import Festival
from music_week_app.models import MusicWeek


class IndexView(View):

	def get(self, request):
		context = {
			'kulichi': Category.objects.filter(name='Куличи').first(),
			'vareniki': Category.objects.filter(name='Вареники').first(),
			'festivals': Festival.objects.filter(is_active=True).order_by('-id')[:2],
			'music_week': MusicWeek.objects.filter(date__lte=datetime.datetime.now()).order_by('date').last(),
			'bestsellers' : Bestseller.objects.filter(good__quantity__gte=1).order_by('?'),
		}
		return  render(request, 'baseapp/index.html', context)

class DeliveryView(View):

	def get(self, request):
		return  render(request, 'baseapp/delivery.html')

class AtmosphereView(View):	

	def get(self, request):
		return  render(request, 'baseapp/atmosphere.html')

class AboutUsView(View):

	def get(self, request):
		return  render(request, 'baseapp/about_us.html')

class ContactUsView(View):

	def get(self, request):
		return  render(request, 'baseapp/contact_us.html')

class PromoView(View):

	def get(self, request):
		context = {
			'set_lunch': Good.objects.filter(name="Дружеский обед").first(),
		}
		return  render(request, 'baseapp/promo_obedy.html', context)

class SetLunchView(View):

	def get(self, request):
		now = datetime.datetime.now()
		min_time = '11:00'
		max_time = '18:00'
		min_time_datetime = now.replace(hour=11, minute=0)
		max_time_datetime = now.replace(hour=18, minute=0)
		now_active = False
		if min_time_datetime < now < max_time_datetime:
			now_active = True
			if now < (max_time_datetime - datetime.timedelta(minutes=30)):
				min_time = (now + datetime.timedelta(minutes=30)).strftime('%H:%M')
			else:
				min_time = max_time
		context = {
			'min_time': min_time,
			'max_time': max_time,
			'now_active': now_active,
			'set_lunch': Set_Lunch.objects.filter(date=now).first(),
			'good_slug': Good.objects.filter(name="Дружеский обед").first().slug,
		}
		return  render(request, 'baseapp/set_lunch.html', context)

class GiftBoxesView(View):

	def get(self, request):
		return  render(request, 'baseapp/gift_boxes.html')

class BreakfastView(View):

	def get(self, request):
		context = {
			'breakfast_menu': Breakfast.objects.all().first(),
			'bestsellers' : Bestseller.objects.filter(good__quantity__gte=1).order_by('?'),
		}
		return render(request, 'baseapp/breakfasts.html', context)	

class CertificateView(View):

	def get(self, request):
		context = {
			'category': Category.objects.filter(name='Сертификаты').first(),
			'bestsellers' : Bestseller.objects.filter(good__quantity__gte=1).order_by('?'),
		}
		return  render(request, 'baseapp/certificate.html', context)
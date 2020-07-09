from django.shortcuts import render
from .models import Good, Picture, Object_property_values, Properties, Property_value
from .models import Category, Manufacturer, In_Barrels

from cartapp.models import Cart, Cart_Item

from django.core.paginator import Paginator

from django.db.models import Sum

from wishlistapp.views import get_wishlist
from wishlistapp.models import Wishlist, Wishlist_Item


def get_cart_(request):

	if request.user.is_authenticated:
		cart 		= Cart.objects.filter(user = request.user).last()
	else:
		cart_id 	= request.session.get("cart_id")	
		cart 		= Cart.objects.filter(id = cart_id).last()

	return cart


def get_in_barrels():

	in_bar = In_Barrels.objects.all()[:8]

	table = []

	for good in in_bar:

		item = Item()

		item.good = good.good
		
		images = Picture.objects.filter(good=good.good, main_image=True).first()
		if images:
			item.image = images
		else:
			item.image = Picture.objects.filter(good=good.good).first()
		 	
		table.append(item)

	return table	

class Item(object):
	
	good 	= Good
	image 	= Picture

def show_catalog(request):

	goods_count=20

	goods = Good.objects.filter(is_active=True)
	
	table = []
	for good in goods:

		item = Item()
		
		item.good = good
		
		images = Picture.objects.filter(good=good, main_image=True).first()
		if images:
			item.image = images
		else:
			item.image = Picture.objects.filter(good=good).first()
		 	
		table.append(item)	

	page_number = request.GET.get('page', 1)

	paginator = Paginator(table, goods_count)	

	page = paginator.get_page(page_number)


	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''			

	wishlist = []
	for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
		wishlist.append(item.good)

	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'cart': get_cart_(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		'wishlist' : wishlist,
	}
	


	return render(request, template_name, context)

def show_good(request, slug):

	good = Good.objects.get(slug=slug)
		
	pictures = Picture.objects.filter(good=good).order_by('-main_image')
	main_pictures = pictures.first()


	opv = Object_property_values.objects.filter(good=good)
	is_cidre = False
	# Страна
	country = opv.filter(_property=Properties.objects.filter(slug='728193372').first()).first()
	if country:
		country = country.property_value
		is_cidre = True
	else:
		country = ''
	# Крепость
	strength = opv.filter(_property=Properties.objects.filter(slug='202312845').first()).first()
	if strength:
		strength = strength.property_value
		is_cidre = True
	else:
		strength = ''
	# Сахар
	sugar = opv.filter(_property=Properties.objects.filter(slug='2193900133').first()).first()
	if sugar:
		sugar = sugar.property_value
		is_cidre = True
	else:
		sugar = ''
	# Объем
	volume = opv.filter(_property=Properties.objects.filter(slug='3824689493').first()).first()
	if volume:
		volume = volume.property_value
		is_cidre = True
	else:
		volume = ''
	# Газация
	gas = opv.filter(_property=Properties.objects.filter(slug='1240764269').first()).first()
	if gas:
		gas = gas.property_value
		is_cidre = True
	else:
		gas = ''
	# Пастеризация
	pasteuriz = opv.filter(_property=Properties.objects.filter(slug='2448919171').first()).first()
	if pasteuriz:
		pasteuriz = pasteuriz.property_value
		is_cidre = True
	else:
		pasteuriz = ''
	# Фильтрация
	filtration = opv.filter(_property=Properties.objects.filter(slug='1716778945').first()).first()
	if filtration:
		filtration = filtration.property_value
		is_cidre = True
	else:
		filtration = ''
	# Что внутри?
	inside = opv.filter(_property=Properties.objects.filter(slug='552212307').first()).first()
	if inside:
		inside = inside.property_value
		is_cidre = True
	else:
		inside = ''	


	wishlist = []
	for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
		wishlist.append(item.good)

	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)

	template_name = 'goodapp/good.html'

	context = {
	
		'good': good, 'pictures': pictures, 'main_pictures': main_pictures, 'opv': opv,
		'country':country,
		'strength':strength,
		'sugar':sugar,
		'volume':volume,
		'gas':gas,
		'pasteuriz':pasteuriz,
		'filtration':filtration,
		'inside': inside,
		'is_cidre': is_cidre,
		'cart': get_cart_(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		'wishlist' : wishlist,

	}
	return render(request, template_name, context)

def show_category(request, slug):

	if slug == '4127154760':

		try:
			category = Category.objects.get(slug=slug)
		except:
			category = None

		subcategories = Category.objects.filter(parent_category=category).order_by('rank')

		wishlist = []
		for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
			wishlist.append(item.good)

		template_name = 'goodapp/catalog.html'

		context = {
			'subcategories': subcategories, 'category': category,
			'cart': get_cart_(request),
			'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
			'wishlist' : wishlist,

		}
		
	else:	
		goods_count=20

		try:
			category = Category.objects.get(slug=slug)
		except:
			category = None

		goods = Good.objects.filter(category=category, is_active=True)
		
		table = []
		for good in goods:

			item = Item()
			
			item.good = good
			
			images = Picture.objects.filter(good=good, main_image=True).first()
			if images:
				item.image = images
			else:
				item.image = Picture.objects.filter(good=good).first()
			 	
			table.append(item)	

		page_number = request.GET.get('page', 1)

		paginator = Paginator(table, goods_count)	

		page = paginator.get_page(page_number)


		is_paginated = page.has_other_pages()

		if page.has_previous():
			prev_url = '?page={}'.format(page.previous_page_number())
		else:
			prev_url = ''	

		if page.has_next():
			next_url = '?page={}'.format(page.next_page_number())
		else:
			next_url = ''			

		wishlist = []
		for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
			wishlist.append(item.good)

		barrels = []
		for item in In_Barrels.objects.all():
			barrels.append(item.good)	


		template_name = 'goodapp/catalog.html'
		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'category': category,
			'cart': get_cart_(request),
			'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'barrels': barrels,
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
			'wishlist' : wishlist,
		}

	return render(request, template_name, context)


def show_manufacturer(request, slug):

	goods_count=20

	try:
		manufacturer = Manufacturer.objects.get(slug=slug)
	except:
		manufacturer = None
	
	goods = Good.objects.filter(manufacturer=manufacturer, is_active=True)
	
	table = []
	for good in goods:

		item = Item()
		
		item.good = good
		
		images = Picture.objects.filter(good=good, main_image=True).first()
		if images:
			item.image = images
		else:
			item.image = Picture.objects.filter(good=good).first()
		 	
		table.append(item)	

	page_number = request.GET.get('page', 1)

	paginator = Paginator(table, goods_count)	

	page = paginator.get_page(page_number)


	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''			

	wishlist = []
	for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
		wishlist.append(item.good)

	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)	

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'manufacturer': manufacturer,
		'cart': get_cart_(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		'wishlist' : wishlist,
	}

	return render(request, template_name, context)




def show_in_barrels(request):

	wishlist = []
	for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
		wishlist.append(item.good)

	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)

	context = {

		'in_bar': get_in_barrels(),
		'cart': get_cart_(request),
		'barrels': barrels,
		'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		'wishlist' : wishlist,

	}

	
	return render(request, 'goodapp/in_barrels.html', context)


def show_product_with_tag(request):

	goods_count=20

	property_value = Property_value.objects.get(title=request.GET.get('tag'))

	opv = Object_property_values.objects.filter(property_value=property_value)
	
	table = []
	for n in opv:

		if n.good.is_active:
			item = Item()
			
			item.good = n.good
			
			images = Picture.objects.filter(good=n.good, main_image=True).first()
			if images:
				item.image = images
			else:
				item.image = Picture.objects.filter(good=n.good).first()
			 	
			table.append(item)	

	page_number = request.GET.get('page', 1)

	paginator = Paginator(table, goods_count)	

	page = paginator.get_page(page_number)


	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?tag={1}&page={0}'.format(page.previous_page_number(), property_value)
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?tag={1}&page={0}'.format(page.next_page_number(), property_value)
	else:
		next_url = ''			

	wishlist = []
	for item in Wishlist_Item.objects.filter(wishlist=get_wishlist(request)):
		wishlist.append(item.good)

	barrels = []
	for item in In_Barrels.objects.all():
		barrels.append(item.good)


	template_name = 'goodapp/tags.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'cart': get_cart_(request),
		'cart_count' : Cart_Item.objects.filter(cart=get_cart_(request)).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=get_wishlist(request))), 
		'wishlist' : wishlist,
		'property_value': property_value,
	}

	return render(request, template_name, context)
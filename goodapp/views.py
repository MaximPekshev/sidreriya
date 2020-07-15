from django.shortcuts import render
from .models import Good, Picture, Object_property_values, Properties, Property_value
from .models import Category, Manufacturer, In_Barrels

from django.http import HttpResponse

from cartapp.models import Cart, Cart_Item

from django.core.paginator import Paginator

from django.db.models import Sum

from wishlistapp.views import get_wishlist
from wishlistapp.models import Wishlist, Wishlist_Item

# from django.core.exceptions import ObjectDoesNotExis


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

def get_filters():

	filters = []

	manufacturers = {}

	for man in Manufacturer.objects.all():
		manufacturers.update({man.slug : man.name})

	price = []

	country 	= {}
	what_inside = {}
	sugar 		= {}
	gas 		= {}
	pasteuriz 	= {}
	filtration 	= {}
	strength 	= dict([(27, 'безалкогольный'), (31, 'до 3%'), (48, 'больше 3%')])
	# dict(nonalc='безалкогольный', alcless3='до 3%', alcmore3='больше 3%')
	volume 		= {}

	for item in Good.objects.filter(is_active=True):

		if item.price not in price:

			if item.price != None:

				price.append(item.price)


	pv = Property_value.objects.all()

	for item_opv in pv:
		if item_opv != None:
			# Страна
			if item_opv._property.slug == '728193372':
				if item_opv.id not in country.keys():
					country.update({item_opv.id : item_opv.title})
			# Крепость
			# elif item_opv._property.slug == '202312845':
			# 	if item_opv.id not in strength.keys():
			# 		strength.update({item_opv.id : item_opv.title})
			# Сахар
			elif item_opv._property.slug == '2193900133':
				if item_opv.id not in sugar.keys():
					sugar.update({item_opv.id : item_opv.title})
			# Объем
			elif item_opv._property.slug == '3824689493':
				if item_opv.id not in volume.keys():
					volume.update({item_opv.id : item_opv.title})
			# Газация
			elif item_opv._property.slug == '1240764269':
				if item_opv.id not in gas.keys():
					gas.update({item_opv.id : item_opv.title})
			# Пастеризация
			elif item_opv._property.slug == '2448919171':
				if item_opv.id not in pasteuriz.keys():
					pasteuriz.update({item_opv.id : item_opv.title})
			# Фильтрация
			elif item_opv._property.slug == '1716778945':
				if item_opv.id not in filtration.keys():
					filtration.update({item_opv.id : item_opv.title})
			# Что внутри?
			elif item_opv._property.slug == '552212307':
				if item_opv.id not in what_inside.keys():
					what_inside.update({item_opv.id : item_opv.title})													

	price.sort()

	filters.append(manufacturers)
	filters.append(price)
	filters.append(country)
	filters.append(strength)
	filters.append(sugar)
	filters.append(volume)
	filters.append(gas)
	filters.append(pasteuriz)
	filters.append(filtration)
	filters.append(what_inside)

	return filters	

class Item(object):
	
	good 	= Good
	image 	= Picture

def show_catalog(request):

	goods_count=20

	goods = Good.objects.filter(is_active=True)

	filters = get_filters()
	
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
		'filters' : filters,
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

		if category.name == 'Сидр':
			filters = get_filters()
		else:
			filters = None	

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
			'filters' : filters,
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


def show_product_with_filters(request):

	
	if request.method == 'GET':

		goods_count=20

		table = []

		goods = []

		for good in Good.objects.all():
			goods.append(good)

		active_filters = {}

		temp_table = []

		for f_item in request.GET:

			if f_item != 'page':

				if f_item == '31':

					f_goods = []

					active_filters.update({31:'до 3%'})

					property_values = Property_value.objects.filter(pk__in=[28,29,30,31,68])

					for pv in property_values:

						for opv in Object_property_values.objects.filter(property_value=pv):

							if opv.good.is_active == True:

								f_goods.append(opv.good)


					temp_table = list(set(goods)&set(f_goods))
							
					goods = temp_table		

				elif f_item == '48':

					f_goods = []

					active_filters.update({48:'больше 3%'})

					property_values = Property_value.objects.filter(pk__in=[32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53])

					for pv in property_values:

						for opv in Object_property_values.objects.filter(property_value=pv):

							if opv.good.is_active == True:

								f_goods.append(opv.good)
								

					temp_table = list(set(goods)&set(f_goods))
							
					goods = temp_table

				else:	

					try:
						property_value = Property_value.objects.get(id=f_item)

						if f_item == '27':

							active_filters.update({27:'безалкогольный'})

						else: 

							active_filters.update({property_value.id : property_value.title})

						f_goods = []

						for opv in Object_property_values.objects.filter(property_value=property_value):

							if opv.good.is_active == True:

								f_goods.append(opv.good)

						temp_table = list(set(goods)&set(f_goods))

						goods = temp_table	

					except Property_value.DoesNotExist:
						
						try:

							manufacturer = Manufacturer.objects.get(slug=f_item)

							active_filters.update({manufacturer.slug : manufacturer.name})

							f_goods = []

							for good in Good.objects.filter(manufacturer=manufacturer, is_active=True):

								f_goods.append(good)

							temp_table = list(set(goods)&set(f_goods))

							goods = temp_table

						except Manufacturer.DoesNotExist:

							pass

		if not active_filters:

			for good in Good.objects.filter(is_active=True):
				temp_table.append(good)



		for n in temp_table:

			if n.is_active:

				item = Item()

				item.good = n
				
				images = Picture.objects.filter(good=n, main_image=True).first()
				if images:
					item.image = images
				else:
					item.image = Picture.objects.filter(good=n).first()
				 	
				table.append(item)



		filters = get_filters()
		
		page_number = request.GET.get('page', 1)

		paginator = Paginator(table, goods_count)	

		page = paginator.get_page(page_number)

		str_active_filters = '?'
		for key, value in active_filters.items():
			str_active_filters += str(key) + '=' + str(value) + '&'

		is_paginated = page.has_other_pages()

		if page.has_previous():
			prev_url = '{1}page={0}'.format(page.previous_page_number(), str_active_filters)
		else:
			prev_url = ''	

		if page.has_next():
			next_url = '{1}page={0}'.format(page.next_page_number(), str_active_filters)
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
			'filters' : filters,
			'active_filters':active_filters.values(),
			'str_active_filters': str_active_filters,
		}

		return render(request, template_name, context) 	
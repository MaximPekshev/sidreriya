from django.shortcuts import render
from .models import Good, Picture, Object_property_values, Properties, Property_value
from .models import Category, Manufacturer, In_Barrels, Bestseller

from django.http import HttpResponse

from cartapp.models import Cart, Cart_Item

from django.core.paginator import Paginator

from django.db.models import Sum

from wishlistapp.views import get_wishlist
from wishlistapp.models import Wishlist, Wishlist_Item

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GoodSerializer

from filterapp.models import PropertiesFilter

from django.db.models import Q


def get_goods_of_object_property_values(property_values, goods_table):

	f_goods = []

	for good in goods_table:

		if good.is_active==True:

			for pv in property_values:

				for opv in Object_property_values.objects.filter(property_value=pv, good=good):

					f_goods.append(opv.good)

	return f_goods

def get_goods_of_single_object_property_value(property_value, goods_table):

	f_goods = []

	for good in goods_table:

		if good.is_active==True:

			for opv in Object_property_values.objects.filter(property_value=property_value, good=good):

				f_goods.append(opv.good)

	return f_goods	



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


def get_filters_a(goods_table=[]):

	filters = []

	properties_filter = PropertiesFilter.objects.all().order_by('-pk')

	if properties_filter:

		for pf in properties_filter:

			property_value = Property_value.objects.filter(_property=pf.p_filter) 

			if property_value:

				filter_values = []

				for pv in property_value:

					opv = Object_property_values.objects.filter(property_value=pv)

					# goods_with_opv = []

					# for item in opv:
					# 	if item.good.is_active == True and item.good in goods_table:
					# 		goods_with_opv.append(item.good)


					# filter_values.append([pv.title, len(goods_with_opv)])
					filter_values.append([pv.title, 1])

				dict_filters_values = dict.fromkeys([pf.p_filter.title], filter_values)
				
				filters.append(dict_filters_values)

	# filters.append(dict.fromkeys(
	# 	['Крепость'],
	# 	 [['безалкогольный', len(get_goods_of_single_object_property_value(Property_value.objects.get(pk=27), goods_table))],
	# 	  ['до 3%', len(get_goods_of_object_property_values(Property_value.objects.filter(pk__in=[28,29,30,31,68]), goods_table))],
	# 	  ['больше 3%', len(get_goods_of_object_property_values(Property_value.objects.filter(pk__in=[32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]), goods_table))]
	# 	  ]
	# 	  )
	# )
	filters.append(dict.fromkeys(
		['Крепость'],
		 [['безалкогольный', 1],
		  ['до 3%', 2],
		  ['больше 3%', 3]
		  ]
		  )
	)

	manufacturers = Manufacturer.objects.all()

	if manufacturers:
		filter_values = []
		for manufacturer in manufacturers:
			filter_values.append([manufacturer.name, 1])

		dict_filters_values = dict.fromkeys(['Производители'], filter_values)
				
		filters.append(dict_filters_values)

	return filters


class Item(object):
	
	good 	= Good
	image 	= Picture

def get_items_with_pictures(goods):

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

	return table	


def query_set_to_list(q_set):
	
	my_list = []

	for item in q_set:
		my_list.append(item.good)

	return my_list	


def show_catalog(request):

	goods_count=18

	goods = Good.objects.filter(is_active=True).order_by('price')
	
	page_number = request.GET.get('page', 1)

	table = get_items_with_pictures(goods)

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

	current_wishlist = get_wishlist(request)

	wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
	barrels = query_set_to_list(In_Barrels.objects.all())

	current_cart = 	get_cart_(request)

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'cart': current_cart,
		'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
		'wishlist' : wishlist,
		'filters_a' : get_filters_a(goods),
	}
	
	return render(request, template_name, context)


def get_object_property_value(opv, slug):

	value = opv.filter(_property=Properties.objects.filter(slug=slug).first()).first()

	if value:
		value = value.property_value
	else:
		value = ''

	return value		




def show_good(request, slug):

	good = Good.objects.get(slug=slug)
		
	pictures = Picture.objects.filter(good=good).order_by('-main_image')
	main_pictures = pictures.first()


	opv = Object_property_values.objects.filter(good=good)
	# Страна
	country = get_object_property_value(opv, '728193372')
	# Крепость
	strength = get_object_property_value(opv, '202312845')
	# Сахар
	sugar = get_object_property_value(opv, '2193900133')
	# Объем
	volume = get_object_property_value(opv, '3824689493')
	# Газация
	gas = get_object_property_value(opv, '1240764269')
	# Пастеризация
	pasteuriz = get_object_property_value(opv, '2448919171')
	# Фильтрация
	filtration = get_object_property_value(opv, '1716778945')
	# Что внутри?
	inside = get_object_property_value(opv, '552212307')

	current_wishlist = 	get_wishlist(request)

	wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
	barrels = query_set_to_list(In_Barrels.objects.all())

	current_cart = get_cart_(request)

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
		'is_cidre': good.is_cidre,
		'cart': get_cart_(request),
		'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
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

		current_wishlist = 	get_wishlist(request)

		wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
		current_cart = get_cart_(request)

		template_name = 'goodapp/catalog.html'

		context = {
			'subcategories': subcategories, 'category': category,
			'cart': current_cart,
			'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
			'wishlist' : wishlist,

		}
		
	elif slug == '481372718':

		goods_count=18

		try:
			category = Category.objects.get(slug=slug)
		except:
			category = None	

		goods = Good.objects.filter(category=category)

		table = get_items_with_pictures(goods)

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

		current_wishlist = 	get_wishlist(request)

		wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
		barrels = query_set_to_list(In_Barrels.objects.all())

		current_cart = get_cart_(request)

		template_name = 'goodapp/catalog.html'

		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'category': category,
			'cart': current_cart,
			'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
			'wishlist' : wishlist,
		}	
	elif slug == '440621953':

		goods_count=18

		try:
			category = Category.objects.get(slug=slug)
		except:
			category = None	

		goods = Good.objects.filter(category=category)

		table = get_items_with_pictures(goods)

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

		current_wishlist = 	get_wishlist(request)

		wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
		barrels = query_set_to_list(In_Barrels.objects.all())

		current_cart = get_cart_(request)

		template_name = 'goodapp/catalog.html'

		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'category': category,
			'cart': current_cart,
			'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
			'wishlist' : wishlist,
		}
		
	else:

		goods_count=18

		try:
			category = Category.objects.get(slug=slug)
		except:
			category = None	

		goods = Good.objects.filter(category=category, is_active=True).order_by('price')

		if category.name == 'Сидр':
			filters_a = get_filters_a(goods)
			bestsellers = Bestseller.objects.all().order_by('?')
		else:
			filters_a = None
			bestsellers = None
		
		table = get_items_with_pictures(goods)

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

		current_wishlist = 	get_wishlist(request)

		wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
		barrels = query_set_to_list(In_Barrels.objects.all())

		current_cart = get_cart_(request)

		template_name = 'goodapp/catalog.html'

		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'category': category,
			'cart': current_cart,
			'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'barrels': barrels,
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
			'wishlist' : wishlist,
			'filters_a' : filters_a,
			'bestsellers' : bestsellers,
		}

	return render(request, template_name, context)


def show_manufacturer(request, cpu_slug):

	goods_count=18

	try:
		manufacturer = Manufacturer.objects.get(cpu_slug=cpu_slug)
	except:
		manufacturer = None
	
	goods = Good.objects.filter(manufacturer=manufacturer, is_active=True).order_by('price')
	
	table = get_items_with_pictures(goods)

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

	current_wishlist = 	get_wishlist(request)

	wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
	barrels = query_set_to_list(In_Barrels.objects.all())

	current_cart = get_cart_(request)

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'manufacturer': manufacturer,
		'cart': current_cart,
		'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
		'wishlist' : wishlist,
	}

	return render(request, template_name, context)



def show_in_barrels(request):

	current_wishlist = 	get_wishlist(request)

	wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
	barrels = query_set_to_list(In_Barrels.objects.all())

	current_cart = get_cart_(request)

	context = {

		'in_bar': get_in_barrels(),
		'cart': current_cart,
		'barrels': barrels,
		'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
		'wishlist' : wishlist,

	}

	
	return render(request, 'goodapp/in_barrels.html', context)


def show_product_with_tag(request):

	goods_count=18

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

	current_wishlist = 	get_wishlist(request)

	wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
	barrels = query_set_to_list(In_Barrels.objects.all())

	current_cart = get_cart_(request)


	template_name = 'goodapp/tags.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'cart': current_cart,
		'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
		'in_bar': get_in_barrels(),
		'barrels': barrels,
		'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
		'wishlist' : wishlist,
		'property_value': property_value,
	}

	return render(request, template_name, context)


def show_product_with_filters(request):

	
	if request.method == 'GET':

		goods_count=18

		table = []

		goods = Good.objects.all().order_by('price')

		active_filters = []

		temp_table = []

		str_active_filters = '?'

		for item in request.GET:

			goods_in_filter_group = []

			if item != 'page':

				if item == 'Крепость':
					
					for f_item in request.GET.getlist('Крепость'):
						
						if f_item == 'до 3%':

							property_value = Property_value.objects.filter(pk__in=[28,29,30,31,68])

							active_filters.append('до 3%')

							str_active_filters += 'Крепость=до 3%&'

							goods_with_opv = get_goods_of_object_property_values(property_value, Good.objects.filter(is_active=True))
						
							for i in goods_with_opv:

								goods_in_filter_group.append(i)

						elif f_item == 'больше 3%':

							active_filters.append('больше 3%')

							str_active_filters += 'Крепость=больше 3%&'

							property_value = Property_value.objects.filter(pk__in=[32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53])
										
							goods_with_opv = get_goods_of_object_property_values(property_value, Good.objects.filter(is_active=True))
						
							for i in goods_with_opv:

								goods_in_filter_group.append(i)

						elif f_item == 'безалкогольный':


							active_filters.append('безалкогольный')

							str_active_filters += 'Крепость=безалкогольный&'

							property_value = Property_value.objects.get(pk=27)
										
							goods_with_opv = get_goods_of_single_object_property_value(property_value, Good.objects.filter(is_active=True))
						
							for i in goods_with_opv:

								goods_in_filter_group.append(i)

				elif item == 'Производители':

					for f_item in request.GET.getlist('Производители'):

						try:
							manufacturer = Manufacturer.objects.get(name=f_item)

							active_filters.append(manufacturer.name)

							str_active_filters += 'Производители=' + str(f_item) + '&'

							goods_with_filter = Good.objects.filter(manufacturer=manufacturer, is_active=True)

							for good in goods_with_filter:

								goods_in_filter_group.append(good)

						except Manufacturer.DoesNotExist:

							pass

				else:

					for f_item in request.GET.getlist(item):

						try:
							property_value = Property_value.objects.get(title=f_item)
							
							active_filters.append(property_value.title)

							str_active_filters += str(item) + '=' + str(f_item) + '&'

							goods_with_opv = get_goods_of_single_object_property_value(property_value, Good.objects.filter(is_active=True))
							
							for i in goods_with_opv:

								goods_in_filter_group.append(i)	
							
						except Property_value.DoesNotExist:

							pass

				temp_table = list(set(goods)&set(goods_in_filter_group))

				goods = temp_table	
		

		if not active_filters:

			try:
				category = Category.objects.get(name='Сидр')

				temp_table = Good.objects.filter(category=category, is_active=True).order_by('price')

			except Category.DoesNotExist:

				temp_table = Good.objects.filter(is_active=True).order_by('price')
				


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

		
		page_number = request.GET.get('page', 1)

		paginator = Paginator(table, goods_count)	

		page = paginator.get_page(page_number)

		is_paginated = page.has_other_pages()


		if page.has_previous():
			prev_url = '{1}page={0}'.format(page.previous_page_number(), str_active_filters)
		else:
			prev_url = ''	

		if page.has_next():
			next_url = '{1}page={0}'.format(page.next_page_number(), str_active_filters)
		else:
			next_url = ''			

		current_wishlist = 	get_wishlist(request)

		wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
		barrels = query_set_to_list(In_Barrels.objects.all())

		current_cart = get_cart_(request)

		template_name = 'goodapp/catalog.html'
		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'cart': current_cart,
			'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'barrels': barrels,
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
			'wishlist' : wishlist,
			'filters_a' : get_filters_a(temp_table),
			'active_filters': active_filters,
			'str_active_filters': str_active_filters,
			'bestsellers' : get_items_with_pictures(query_set_to_list(Bestseller.objects.all().order_by('?'))),
		}

		return render(request, template_name, context) 

def show_search_result(request):
	
	if request.method == 'GET':

		query = request.GET.get('q')

		goods = Good.objects.filter(

			Q(name__icontains=query) |
			Q(name__icontains=query.upper()) |
			Q(name__icontains=query.lower()) |
			Q(name__icontains=query.capitalize()) |
			Q(name_en__icontains=query) |
			Q(name_en__icontains=query.upper()) |
			Q(name_en__icontains=query.lower()) |
			Q(name_en__icontains=query.capitalize()),
			is_active=True

			)

		goods_count=18

		page_number = request.GET.get('page', 1)

		paginator = Paginator(goods, goods_count)

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

		current_wishlist = get_wishlist(request)

		wishlist = query_set_to_list(Wishlist_Item.objects.filter(wishlist=current_wishlist))
		barrels = query_set_to_list(In_Barrels.objects.all())

		current_cart = 	get_cart_(request)

		template_name = 'goodapp/search.html'
		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'cart': current_cart,
			'cart_count' : Cart_Item.objects.filter(cart=current_cart).aggregate(Sum('quantity'))['quantity__sum'],
			'in_bar': get_in_barrels(),
			'barrels': barrels,
			'wishlist_count' : len(Wishlist_Item.objects.filter(wishlist=current_wishlist)), 
			'wishlist' : wishlist,
			'filters_a' : get_filters_a(goods),
			'q' : query,
		}
		
		return render(request, template_name, context)
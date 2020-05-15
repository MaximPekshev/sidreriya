from django.shortcuts import render
from .models import Good, Picture, Object_property_values, Properties
from .models import Category, Manufacturer

from django.core.paginator import Paginator

class Item(object):
	
	good 	= Good
	image 	= Picture

def show_catalog(request):

	goods_count=12

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


	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
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

	template_name = 'goodapp/good.html'

	context = {
	
		'good': good, 'pictures': pictures, 'main_pictures': main_pictures,
		'country':country,
		'strength':strength,
		'sugar':sugar,
		'volume':volume,
		'gas':gas,
		'pasteuriz':pasteuriz,
		'filtration':filtration,
		'inside': inside,
		'is_cidre': is_cidre,

	}
	return render(request, template_name, context)

def show_category(request, slug):

	if slug == '4127154760':

		try:
			category = Category.objects.get(slug=slug)
		except:
			category = None

		subcategories = Category.objects.filter(parent_category=category).order_by('rank')

		template_name = 'goodapp/catalog.html'

		context = {
			'subcategories': subcategories, 'category': category,
		}
		
	else:	
		goods_count=12

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


		template_name = 'goodapp/catalog.html'
		context = {
			'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
			'category': category,
		}

	return render(request, template_name, context)


def show_manufacturer(request, slug):

	goods_count=12

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


	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'manufacturer': manufacturer,
	}

	return render(request, template_name, context)		
from django.shortcuts import render
from .models import Good, Picture, Object_property_values, Properties
from .models import Category, Manufacturer

from django.core.paginator import Paginator

class Item(object):
	
	good 	= Good
	image 	= Picture

def show_catalog(request):

	goods_count=12

	goods = Good.objects.all()
	
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

	categories = Category.objects.all()	

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'categories': categories,
	}
	


	return render(request, template_name, context)

def show_good(request, slug):

	good = Good.objects.get(slug=slug)
		
	pictures = Picture.objects.filter(good=good).order_by('-main_image')
	main_pictures = pictures.first()


	opv = Object_property_values.objects.filter(good=good)

	country = opv.filter(_property=Properties.objects.filter(title='Страна').first()).first()
	if country:
		country = country.property_value
	else:
		country = ''

	strength = opv.filter(_property=Properties.objects.filter(title='Крепость').first()).first()
	if strength:
		strength = strength.property_value
	else:
		strength = ''

	sugar = opv.filter(_property=Properties.objects.filter(title='Сахар').first()).first()
	if sugar:
		sugar = sugar.property_value
	else:
		sugar = ''

	volume = opv.filter(_property=Properties.objects.filter(title='Объем').first()).first()
	if volume:
		volume = volume.property_value
	else:
		volume = ''

	gas = opv.filter(_property=Properties.objects.filter(title='Газация').first()).first()
	if gas:
		gas = gas.property_value
	else:
		gas = ''

	pasteuriz = opv.filter(_property=Properties.objects.filter(title='Пастеризация').first()).first()
	if pasteuriz:
		pasteuriz = pasteuriz.property_value
	else:
		pasteuriz = ''

	filtration = opv.filter(_property=Properties.objects.filter(title='Фильтрация').first()).first()
	if filtration:
		filtration = filtration.property_value
	else:
		filtration = ''

	categories = Category.objects.all()

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
		'categories': categories,

	}
	return render(request, template_name, context)

def show_category(request, slug):

	goods_count=12

	try:
		category = Category.objects.get(slug=slug)
	except:
		category = None
	
	goods = Good.objects.filter(category=category)
	
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

	categories = Category.objects.all()	

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'categories': categories, 'category': category,
	}

	return render(request, template_name, context)


def show_manufacturer(request, slug):

	goods_count=12

	try:
		manufacturer = Manufacturer.objects.get(slug=slug)
	except:
		manufacturer = None
	
	goods = Good.objects.filter(manufacturer=manufacturer)
	
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

	categories = Category.objects.all()	

	template_name = 'goodapp/catalog.html'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
		'categories': categories, 'manufacturer': manufacturer,
	}

	return render(request, template_name, context)		
from django.shortcuts import (
    render, 
    get_object_or_404, 
    redirect
)
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal

from goodapp.models import (
	Good,  
	Object_property_values,
	Properties, 
	Property_value,
	Category,
	Manufacturer,
	In_Barrels,
	Bestseller
)
from filterapp.models import PropertiesFilter


def filters(goods, categories_name = [], manufacturers_name = []):
	filters = []
	if categories_name:
		categories = Category.objects.filter(name__in = categories_name)
	else:
		categories_name = ['Сидр', 'Вино']
		categories = Category.objects.filter(name__in = categories_name)	
	filters.append({
		'title': 'Категория',
		'values': [{
			'id': item.pk,
			'title': item.name
		} for item in categories if categories]
	})
	filters.append(
		{
			'title': 'Крепость',
			'values': [
				{'id': 1, 'title': 'безалкогольный'},
				{'id': 2, 'title': 'до 3%'},
				{'id': 3, 'title': 'больше 3%'}
			]	
		}
	)
	properties_filter = PropertiesFilter.objects.all().exclude(p_filter__title='Крепость')
	for item in properties_filter:
		props = list(set(Object_property_values.objects.filter(
				_property=item.p_filter,
				good__in=goods
			).order_by('pk').values_list('property_value', flat=True)))
		props_list = [{
			"id": Property_value.objects.filter(pk=item).first().pk,
			"title": Property_value.objects.filter(pk=item).first().title,
		} for item in props if item != None]
		filters.append(
			{ 
				'title' : item.p_filter.title,
				'values': props_list
			}
		)
	if 	manufacturers_name:
		manufacturers = Manufacturer.objects.filter(name__in = manufacturers_name)
	else:
		manufacturers = Manufacturer.objects.all()
	if manufacturers:
		filters.append(
			{	
				'title': 'Производитель',
				'values': [{
					'id': item.pk,
					'title': item.name
				} for item in manufacturers]
			}
		)
	return filters

# class CatalogView(View):
	
# 	def get(self, request, goods_count=32):
# 		goods = Good.objects.filter(is_active=True).order_by('pk')
# 		page_number = request.GET.get('page', 1)
# 		paginator = Paginator(goods, goods_count)
# 		page = paginator.get_page(page_number)
# 		is_paginated = page.has_other_pages()
# 		if page.has_previous():
# 			prev_url = '?page={}'.format(page.previous_page_number())
# 		else:
# 			prev_url = ''	
# 		if page.has_next():
# 			next_url = '?page={}'.format(page.next_page_number())
# 		else:
# 			next_url = ''
# 		barrels = In_Barrels.objects.all()
# 		context = {
# 			'page_object': page, 
# 			'prev_url': prev_url, 
# 			'next_url': next_url, 
# 			'is_paginated': is_paginated,
# 			'barrels': barrels,
# 			'filters' : filters(goods),
# 		}
# 		return render(request, 'goodapp/catalog.html', context)

class CatalogView(View):

	def get(self, request, goods_count=33):
		active_filters = []
		str_active_filters = '?'
		goods = Good.objects.filter(is_active=True)
		# goods_id_list = []
		category_values = []
		manufacturer_values = []
		for filter in request.GET:
			if filter == 'page':
				continue
			elif filter == 'Крепость':
				stranght_values = Property_value.objects.filter(_property__title=filter)
				all_values = list(map(lambda x: Decimal(x.replace(',',  '.')), stranght_values.values_list('title', flat=True)))
				for filter_value in request.GET.getlist('Крепость'):
					if filter_value == 'до 3%':
						values = [item for item in all_values if item <= 3]
						active_filters.append('до 3%')
						str_active_filters += 'Крепость=до 3%&'
					if filter_value == 'больше 3%':
						values = [item for item in all_values if item > 3]
						active_filters.append('больше 3%')
						str_active_filters += 'Крепость=больше 3%&'
					if filter_value == 'безалкогольный':
						values = [item for item in all_values if item == 0]
						active_filters.append('безалкогольный')
						str_active_filters += 'Крепость=безалкогольный&'
				values = [str(item).replace('.', ',') for item in values]
				opv = Object_property_values.objects.filter(_property__title=filter, property_value__title__in=values)
				goods = Good.objects.filter(pk__in=opv.values_list('good', flat=True))
				# goods_id_list.append(opv.values_list('good', flat=True))
			elif filter == 'Производитель':
				manufacturer_values = request.GET.getlist('Производитель')
				for filter_value in manufacturer_values:
					active_filters.append(filter_value)
					# filtered_goods = 
					# goods_id_list.append(filtered_goods)
					str_active_filters += 'Производитель={}&'.format(filter_value)
				# print(manufacturer_values)
				goods = Good.objects.filter(pk__in=Good.objects.filter(manufacturer__name__in=manufacturer_values).values_list('pk', flat=True))	
			elif filter == 'Категория':
				category_values = request.GET.getlist(filter)
				for item in category_values:
					active_filters.append(item)
					str_active_filters += 'Категория={}&'.format(item)
				# goods_id_list.append()
				goods = Good.objects.filter(pk__in=Good.objects.filter(category__name__in=category_values).values_list('pk', flat=True))
			else:
				filter_values = request.GET.getlist(filter)
				for item in filter_values:
					active_filters.append(item)
					str_active_filters += '{}={}&'.format(filter, item)
				opv = Object_property_values.objects.filter(_property__title=filter, property_value__title__in=filter_values)
				goods = Good.objects.filter(pk__in=opv.values_list('good', flat=True))
				# goods_id_list.append(opv.values_list('good', flat=True))
		# if active_filters:
		# 	goods = Good.objects.filter(pk__in=goods_id_list, is_active=True).order_by('pk')
		# else:
		# 	goods = Good.objects.filter(is_active=True).order_by('pk')
		page_number = request.GET.get('page', 1)
		paginator = Paginator(goods.order_by('pk'), goods_count)	
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
		barrels = In_Barrels.objects.all()
		context = {
			'page_object': page, 
			'prev_url': prev_url, 
			'next_url': next_url, 
			'is_paginated': is_paginated,
			'barrels': barrels,
			'filters' : filters(goods, category_values, manufacturer_values),
			'active_filters': active_filters,
			'str_active_filters': str_active_filters,
			'bestsellers' : Bestseller.objects.all().order_by('?'),
		}
		return render(request, 'goodapp/catalog.html', context)


def get_object_property_value(opv, title):
	value = opv.filter(_property=Properties.objects.filter(title=title).first()).first()
	if value:
		return value.property_value
	return None

class GoodView(View):

	def get(self, request, slug):
		good = get_object_or_404(Good, slug=slug)
		opv = Object_property_values.objects.filter(good=good)
		if good.is_cidre:
			# Сахар
			sugar = get_object_property_value(opv, 'Сладость')
			# Пастеризация
			pasteuriz = get_object_property_value(opv, 'Пастеризация')
			# Фильтрация
			filtration = get_object_property_value(opv, 'Фильтрация')
			# Что внутри?
			inside = get_object_property_value(opv, 'Что внутри?')
			# Крепость
			strength = get_object_property_value(opv, 'Крепость')
			# Объем
			volume = get_object_property_value(opv, 'Объем бутылочки')
			# Газация
			gas = get_object_property_value(opv, 'Пузырьки')
			# Страна
			country = get_object_property_value(opv, 'Страна')
		if good.is_vine:
			# Сахар
			sugar = get_object_property_value(opv, 'Сладость')
			# Бренд
			brand = get_object_property_value(opv, 'Бренд')
			# Тип
			type = get_object_property_value(opv, 'Тип вина')
			# Виноград
			grapes = get_object_property_value(opv, 'Виноград')
			# Крепость
			strength = get_object_property_value(opv, 'Крепость')
			# Объем
			volume = get_object_property_value(opv, 'Объем бутылочки')
			# Регион
			country = get_object_property_value(opv, 'Регион')
		barrels = In_Barrels.objects.all()

		if good.is_vine:
			template_name = 'goodapp/good_vine.html'
		elif good.is_cidre:
			template_name = 'goodapp/good_cidre.html'
		else:
			template_name = 'goodapp/good.html'				

		context = {
			'good': good, 
			'opv': opv,
			'is_cidre': good.is_cidre,
			'barrels': barrels,

		}
		if good.is_cidre:
			context.update({
				'strength':strength,
				'volume':volume,
				'country':country,
				'sugar':sugar,
				'gas':gas,
				'pasteuriz':pasteuriz,
				'filtration':filtration,
				'inside': inside,
			})
		elif good.is_vine:
			context.update({
				'strength':strength,
				'volume':volume,
				'country':country,
				'sugar':sugar,
				'brand': brand,
				'type': type,
				'grapes': grapes,
			})	
		return render(request, template_name, context)	

class CategoryView(View):

	def get(self, request, slug, goods_count = 32):
		category = get_object_or_404(Category, slug=slug)
		context = {
			'category': category,
		}
		subcategories = Category.objects.filter(parent_category__slug=slug).order_by('rank')
		if subcategories:
			context.update({
				'subcategories': subcategories,
			})
		else:
			goods = Good.objects.filter(category=category, is_active=True).order_by('pk')
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
			barrels = In_Barrels.objects.all()
			if category.name == 'Сидр' or category.name == 'Вино':
				context.update({
					'filters' : filters(goods, categories_name=[category.name]),
					'bestsellers' : Bestseller.objects.all().order_by('?'),
				})
			context.update ({
				'page_object': page, 
				'prev_url': prev_url, 
				'next_url': next_url, 
				'is_paginated': is_paginated,
				'barrels': barrels,
			})
		return render(request, 'goodapp/catalog.html', context)

class ManufacturerView(View):

	def get(self, request, cpu_slug, goods_count = 32):
		manufacturer = get_object_or_404(Manufacturer, cpu_slug=cpu_slug)
		goods = Good.objects.filter(manufacturer=manufacturer, is_active=True).order_by('pk')
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
		barrels = In_Barrels.objects.all()
		context = {
			'page_object': page, 
			'prev_url': prev_url, 
			'next_url': next_url, 
			'is_paginated': is_paginated,
			'manufacturer': manufacturer,
			'barrels': barrels,
		}
		return render(request, 'goodapp/catalog.html', context)

class InBarrelsView(View):

	def get(self, request):
		barrels = In_Barrels.objects.all()
		context = {
			'barrels': barrels,
		}
		return render(request, 'goodapp/in_barrels.html', context)

class TagView(View):

	def get(self, request, goods_count = 32):
		input_tag = request.GET.get('tag')
		opv = Object_property_values.objects.filter(property_value__title=input_tag)
		goods = [ Good.objects.filter(pk=item).first() for item in opv.values_list('good', flat=True)]
		page_number = request.GET.get('page', 1)
		paginator = Paginator(goods, goods_count)	
		page = paginator.get_page(page_number)
		is_paginated = page.has_other_pages()
		if page.has_previous():
			prev_url = '?tag={1}&page={0}'.format(page.previous_page_number(), input_tag)
		else:
			prev_url = ''	
		if page.has_next():
			next_url = '?tag={1}&page={0}'.format(page.next_page_number(), input_tag)
		else:
			next_url = ''			
		barrels = In_Barrels.objects.all()
		context = {
			'page_object': page, 
			'prev_url': prev_url, 
			'next_url': next_url, 
			'is_paginated': is_paginated,
			'barrels': barrels,
			'property_value': input_tag,
		}

		return render(request, 'goodapp/tags.html', context)

class FilteredGoodsView(View):

	def get(self, request, goods_count=32):
		active_filters = []
		str_active_filters = '?'
		goods_id_list = []
		category_values = []
		manufacturer_values = []
		for filter in request.GET:
			if filter == 'page':
				continue
			elif filter == 'Крепость':
				stranght_values = Property_value.objects.filter(_property__title=filter)
				all_values = list(map(lambda x: Decimal(x.replace(',',  '.')), stranght_values.values_list('title', flat=True)))
				for filter_value in request.GET.getlist('Крепость'):
					if filter_value == 'до 3%':
						values = [item for item in all_values if item <= 3]
						active_filters.append('до 3%')
						str_active_filters += 'Крепость=до 3%&'
					if filter_value == 'больше 3%':
						values = [item for item in all_values if item > 3]
						active_filters.append('больше 3%')
						str_active_filters += 'Крепость=больше 3%&'
					if filter_value == 'безалкогольный':
						values = [item for item in all_values if item == 0]
						active_filters.append('безалкогольный')
						str_active_filters += 'Крепость=безалкогольный&'
				values = [str(item).replace('.', ',') for item in values]
				opv = Object_property_values.objects.filter(_property__title=filter, property_value__title__in=values)
				goods_id_list.append(opv.values_list('good', flat=True))
			elif filter == 'Производители':
				manufacturer_values = request.GET.getlist('Производители')
				for filter_value in manufacturer_values:
					active_filters.append(filter_value)
					filtered_goods = Good.objects.filter(manufacturer__name=manufacturer_values).values_list('pk', flat=True)
					goods_id_list.append(filtered_goods)
					str_active_filters += 'Производители={}&'.format(filter_value)
			elif filter == 'Категория':
				category_values = request.GET.getlist(filter)
				for item in category_values:
					active_filters.append(item)
					str_active_filters += 'Категория={}&'.format(item)
				goods_id_list.append(Good.objects.filter(category__name__in=category_values).values_list('pk', flat=True))
			else:
				filter_values = request.GET.getlist(filter)
				for item in filter_values:
					active_filters.append(item)
					str_active_filters += '{}={}&'.format(filter, item)
				opv = Object_property_values.objects.filter(_property__title=filter, property_value__title__in=filter_values)
				goods_id_list.append(opv.values_list('good', flat=True))

		goods = Good.objects.filter(pk__in=goods_id_list, is_active=True).order_by('pk')

		page_number = request.GET.get('page', 1)
		paginator = Paginator(goods, goods_count)	
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
		barrels = In_Barrels.objects.all()
		context = {
			'page_object': page, 
			'prev_url': prev_url, 
			'next_url': next_url, 
			'is_paginated': is_paginated,
			'barrels': barrels,
			'filters' : filters(goods, category_values, manufacturer_values),
			'active_filters': active_filters,
			'str_active_filters': str_active_filters,
			'bestsellers' : Bestseller.objects.all().order_by('?'),
		}
		return render(request, 'goodapp/catalog.html', context)

class SearchView(View):

	def get(self, request, goods_count=32):
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
			).order_by('pk')
		page_number = request.GET.get('page', 1)
		paginator = Paginator(goods, goods_count)
		page = paginator.get_page(page_number)
		is_paginated = page.has_other_pages()
		if page.has_previous():
			prev_url = '?q={}&page={}'.format(query, page.previous_page_number())
		else:
			prev_url = ''	
		if page.has_next():
			next_url = '?q={}&page={}'.format(query, page.next_page_number())
		else:
			next_url = ''			
		barrels = list(In_Barrels.objects.all())
		context = {
			'page_object': page, 
			'prev_url': prev_url, 
			'next_url': next_url, 
			'is_paginated': is_paginated,
			'barrels': barrels,
			'q' : query,
		}
		return render(request, 'goodapp/search.html', context)
from django.shortcuts import (
    render, 
    get_object_or_404
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
from goodapp.services import (
	json_goods_list_from_page_object_list,
	json_good_from_object
)
from baseapp.models import (
    Menu 
)
from filterapp.models import PropertiesFilter


def filters(goods, categories_name = [], manufacturers_name = [], active_filters = None):
	goods_categories = list(dict.fromkeys(goods.values_list('category', flat=True)))
	filters = []
	if categories_name:
		categories = Category.objects.filter(name__in=categories_name, pk__in=goods_categories)
	else:
		categories_name = ['Сидр', 'Вино']
		categories = Category.objects.filter(name__in=categories_name, pk__in=goods_categories)	
	filters.append({
		'title': 'Категория',
		'values': [{
			'id': item.pk,
			'title': item.name
		} for item in categories if categories]
	})
	properties_filter = PropertiesFilter.objects.all().exclude(p_filter__title='Крепость')
	grape_filters = [item.get('value') for item in list(filter(lambda x: x.get('title') == 'Виноград', active_filters))]
	for item in properties_filter:
		props = list(set(Object_property_values.objects.filter(
				_property=item.p_filter,
				good__in=goods
			).order_by('pk').values_list('property_value', flat=True)))
		if item.p_filter.title == 'Виноград' and grape_filters:
			props_title_list = Property_value.objects.filter(pk__in=props).values_list('title', flat=True)
			props_list = [{
				"id": Property_value.objects.filter(title=item).first().pk,
				"title": item,
			} for item in props_title_list if item != None and item in grape_filters]
		else:
			props_list = [{
				"id": item,
				"title": Property_value.objects.filter(pk=item).first().title,
			} for item in props if item != None]	
		filters.append(
			{ 
				'title' : item.p_filter.title,
				'values': props_list
			}
		)
	goods_manufacturers = list(dict.fromkeys(goods.values_list('manufacturer', flat=True)))
	if 	manufacturers_name:
		manufacturers = Manufacturer.objects.filter(name__in = manufacturers_name, pk__in=goods_manufacturers)
	else:
		manufacturers = Manufacturer.objects.filter(pk__in=goods_manufacturers)
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

def min_and_max_straight_values(goods = None):
	# Получаем pk всех уникальных значений свойств крепости
	if goods:
		straight_list_pk = Object_property_values.objects.filter(_property__title='Крепость', good__in=goods).distinct().values_list('property_value', flat=True)
	else:
		straight_list_pk = Object_property_values.objects.filter(_property__title='Крепость').distinct().values_list('property_value', flat=True)	
	# Получаем все значения свойства крепости
	straight_values = Property_value.objects.filter(pk__in=straight_list_pk).values_list('title', flat=True)
	if not straight_values:
		return {
			'max_straight': 15,
			'min_straight': 0,
		}
	# Преобразуем их в числа
	straight_values = list(map(lambda x: Decimal(x.replace(',',  '.')), straight_values))
	# Получаем максимальное значение крепости
	max_straight = max(straight_values)
	# Получаем минимальное значение крепости
	min_straight = min(straight_values)
	return {
		'max_straight': max_straight,
		'min_straight': min_straight,
	}

class CatalogView(View):

	def get(self, request, goods_count=33):
		context = {}
		active_filters = []
		str_active_filters = '?'
		active_filters_obj = []
		goods = Good.objects.filter(is_active=True, category__name__in=["Сидр", "Вино"]).order_by('-pk')
		category_values = []
		manufacturer_values = []
		for filter in request.GET:
			if filter == 'page':
				continue
			elif filter == 'q':
				search_query = request.GET.get('q')
				goods =goods.filter(
						Q(name__icontains=search_query) |
						Q(name__icontains=search_query.upper()) |
						Q(name__icontains=search_query.lower()) |
						Q(name__icontains=search_query.capitalize()) |
						Q(name_en__icontains=search_query) |
						Q(name_en__icontains=search_query.upper()) |
						Q(name_en__icontains=search_query.lower()) |
						Q(name_en__icontains=search_query.capitalize())
					).order_by('pk')
				str_active_filters += 'q={}&'.format(search_query)
				active_filters_obj.append({
					'title': 'q',
					'value': search_query
				})
				context.update({
					'q': search_query,
				})
			elif filter == 'Крепость':
				# получаем значения крепости (min и max)
				straight_values = request.GET.getlist('Крепость')[0].split(',')
				min_straight = Decimal(straight_values[0].replace(',',  '.'))
				max_straight = Decimal(straight_values[1].replace(',',  '.'))
				# получаем все наименования значений крепости
				stranght_values = Property_value.objects.filter(_property__title=filter).values_list('title', flat=True)
				# преобразуем их в числа
				all_values = list(map(lambda x: Decimal(x.replace(',',  '.')), stranght_values))
				# получаем все значения крепости с учетом фильтра
				values = [item for item in all_values if item >= min_straight and item <= max_straight]
				# преобразуем их в строку для дальнейшего поиска по значениям свойств объекта
				values = [str(item).replace('.', ',') for item in values]
				# получаем объекты свойств объекта с учетом фильтра (уникальные)
				opv = Object_property_values.objects.filter(_property__title=filter, property_value__title__in=values).distinct()
				# фильтруем товары по полученным объектам свойств объекта
				goods = goods.filter(pk__in=opv.values_list('good', flat=True))
				context.update({	
					'filter_straight': straight_values,
				})
				str_active_filters += 'Крепость={},{}&'.format(straight_values[0], straight_values[1])
				active_filters.append(straight_values)
			elif filter == 'Производитель':
				manufacturer_values = request.GET.getlist('Производитель')[0].split(',')
				if len(manufacturer_values) == 1 and len(request.GET) == 1:
					context.update({
						'manufacturer': Manufacturer.objects.filter(name=manufacturer_values[0]).first()
					})
				for filter_value in manufacturer_values:
					active_filters.append(filter_value)
					str_active_filters += 'Производитель={}&'.format(filter_value)
					active_filters_obj.append({
						'title': 'Производитель',
						'value': filter_value
					})	
				goods = goods.filter(pk__in=Good.objects.filter(manufacturer__name__in=manufacturer_values).values_list('pk', flat=True))	
			elif filter == 'Категория':
				category_values = request.GET.getlist(filter)[0].split(',')
				for item in category_values:
					active_filters.append(item)
					str_active_filters += 'Категория={}&'.format(item)
					active_filters_obj.append({
						'title': 'Категория',
						'value': item
					})		
				goods = goods.filter(pk__in=Good.objects.filter(category__name__in=category_values).values_list('pk', flat=True))
			elif filter == 'sort':
				sort = request.GET.get('sort')
				if sort == 'price_asc':
					goods = goods.order_by('price')
				elif sort == 'price_desc':
					goods = goods.order_by('-price')
				elif sort == 'newbies':
					goods = goods.order_by('-pk')
				str_active_filters += 'sort={}&'.format(sort)
				active_filters_obj.append({
					'title': 'sort',
					'value': sort
				})
			else:
				filter_values = request.GET.getlist(filter)[0].split(',')
				for item in filter_values:
					active_filters.append(item)
					str_active_filters += '{}={}&'.format(filter, item)
					active_filters_obj.append({
						'title': filter,
						'value': item
					})	
				opv = Object_property_values.objects.filter(_property__title=filter, property_value__title__in=filter_values).distinct()
				goods = goods.filter(pk__in=opv.values_list('good', flat=True))
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
		context.update({
			'page_object': page, 
			'goods_list': json_goods_list_from_page_object_list(request, page.object_list),
			'prev_url': prev_url, 
			'next_url': next_url, 
			'is_paginated': is_paginated,
			'barrels': In_Barrels.objects.all(),
			'filters' : filters(goods, category_values, manufacturer_values, active_filters_obj),
			'active_filters': active_filters,
			'str_active_filters': str_active_filters,
			'active_filters_obj': active_filters_obj,
			'bestsellers' : Bestseller.objects.all().order_by('?'),
			'max_straight': min_and_max_straight_values().get('max_straight'),
			'min_straight': min_and_max_straight_values().get('min_straight'),
			'goods_min_straight': min_and_max_straight_values(goods).get('min_straight'),
			'goods_max_straight': min_and_max_straight_values(goods).get('max_straight')
		})
		return render(request, 'goodapp/catalog.html', context)


def get_object_property_value(opv, title):
	if title == 'Виноград':
		values = opv.filter(_property=Properties.objects.filter(title=title).first())
		return [{
			'value': value.property_value,
			'property': value._property.title
		} for value in values]
	else:
		value = opv.filter(_property=Properties.objects.filter(title=title).first()).first()
		return {
			'value': value.property_value,
			'property': value._property.title,
		} if value else None

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
		context = {
			'good': good, 
			'json_good': json_good_from_object(request, good),
			'opv': opv.exclude(_property__title='Крепость'),
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
		return render(request, 'goodapp/good.html', context)	

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
				'menu': Menu.objects.first(),
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
				'goods_list': json_goods_list_from_page_object_list(request, page.object_list),
				'prev_url': prev_url, 
				'next_url': next_url, 
				'is_paginated': is_paginated,
				'barrels': barrels,
			})
		return render(request, 'goodapp/catalog.html', context)

class InBarrelsView(View):

	def get(self, request):
		barrels = In_Barrels.objects.all()
		context = {
			'barrels': barrels,
		}
		return render(request, 'goodapp/in_barrels.html', context)
import xlrd
import os
from .models import Good, Manufacturer, Category, Properties, Property_value, Object_property_values
from django.core.exceptions import ObjectDoesNotExist


def import_base():
	
	wb = xlrd.open_workbook(os.path.join('tempfiles', 'new_base.xlsx'))
	sheet = wb.sheet_by_index(0)

	for rownum in range(sheet.nrows):
		uid = sheet.cell(rownum, 0).value

		good 				= Good.objects.filter(good_uid=uid).first()

		if good:

			good.name 			= str(sheet.cell(rownum, 2).value)
			good.name_en 		= str(sheet.cell(rownum, 3).value)
			good.description	= str(sheet.cell(rownum, 4).value)
			good.gastronomy 	= str(sheet.cell(rownum, 5).value)
			

			cat = Category.objects.filter(name='Сидр').first()
				
			if cat:

				good.category = cat

			else:

				print('Категория с наименованием Сидр не найдена!!!')

			try:
				man = Manufacturer.objects.get(name=sheet.cell(rownum, 6).value)
				
			except ObjectDoesNotExist:
				print('Производитель с наименованием ', sheet.cell(rownum, 6).value, ' не найден')

			if 	man:

				good.manufacturer = man

			good.save()

			print('изменен товар ', good, 'с УИД' , uid)
			print('---------------------------------------------------------------')
		else:
			print('не найден товар с УИД' , uid)


def get_opv(good, prop, opv):

	inside 	= Properties.objects.filter(title=prop).first()

	if inside:
		pr_value = Property_value.objects.filter(_property=inside, title=opv).first()
		if pr_value:
			opv = Object_property_values.objects.filter(good=good, _property=inside).first()
			if opv:
				opv.property_value = pr_value		
			else:
				opv = Object_property_values(good=good, _property=inside, property_value=pr_value)

			opv.save()


def import_props():
	
	wb = xlrd.open_workbook(os.path.join('tempfiles', 'new_base.xlsx'))
	sheet = wb.sheet_by_index(0)

	for rownum in range(sheet.nrows):
		uid = sheet.cell(rownum, 0).value

		good 	= Good.objects.filter(good_uid=uid).first()

		if good:

			get_opv(good, 'Что внутри?', sheet.cell(rownum, 7).value)	
			get_opv(good, 'Пузырьки', sheet.cell(rownum, 8).value)
			get_opv(good, 'Крепость', sheet.cell(rownum, 9).value)
			get_opv(good, 'Объем бутылочки', sheet.cell(rownum, 10).value)
			get_opv(good, 'Сладость', sheet.cell(rownum, 11).value)
			get_opv(good, 'Страна', sheet.cell(rownum, 12).value)

		else:
			print('не найден товар с УИД' , uid)
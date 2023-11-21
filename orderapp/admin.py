from django.contrib import admin
from django.http import HttpResponse

import csv
from rangefilter.filters import DateTimeRangeFilterBuilder

from .models import Order, Order_Item

class Order_ItemInline(admin.TabularInline):
    model = Order_Item
    extra = 0
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = (
					'date',
					'order_number', 
					'first_name',
					'last_name',
					'phone',
					'email',
					'summ',
					'order_type',
					)
	list_filter = (("date", DateTimeRangeFilterBuilder()), )
	inlines = [Order_ItemInline]
	
	actions = ["export_as_csv"]

	def export_as_csv(self, request, queryset):
		meta = self.model._meta
		field_names = [
			"order_number",
			"first_name",
			"last_name", 
			"phone", 
			"email", 
			"summ", 
		]
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
		writer = csv.writer(response)
		writer.writerow([
			"Дата",
			"Номер заказа",
			"Имя",
			"Фамилия", 
			"Тел.", 
			"email", 
			"Сумма", 
			"Тип заказа"
		])
		for obj in queryset:
			row = [obj.date.strftime("%d %m %Y г. %H:%M")]
			for field in field_names:
				row.append(getattr(obj, field))
			row.append(obj.order_type())
			writer.writerow(row)
		return response

	export_as_csv.short_description = "Выгрузить выбранные"

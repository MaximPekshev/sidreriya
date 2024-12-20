from django.shortcuts import render
from django.views.generic import View
from festapp.models import Festival

class FestivalListView(View):
	
	def get(self, request):
		context = {
			'festivals': Festival.objects.filter(is_active=True).order_by('id'),
		}
		return render(request, 'festapp/fest_list.html', context)

class FestivalView(View):
	
	def get(self, request, cpu_slug):
		context = {
			'festival': Festival.objects.filter(cpu_slug=cpu_slug).first(),
		}
		return render(request, 'festapp/fest.html', context)
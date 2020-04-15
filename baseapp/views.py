from django.shortcuts import render
from goodapp.models import Category

def show_index(request):

	categories = Category.objects.all()

	context = {

			'categories': categories,

	}

	return  render(request, 'baseapp/index.html', context)

from django.shortcuts import render
from django.http import HttpResponse


def show_index(request):

	return  render(request, 'baseapp/index.html')

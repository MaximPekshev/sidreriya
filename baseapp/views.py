from django.shortcuts import render
from goodapp.models import Category

def show_index(request):

	context = {

	}

	return  render(request, 'baseapp/index.html', context)

def show_delivery(request):

	context = {

	}

	return  render(request, 'baseapp/delivery.html', context)	

def show_atmosphere(request):

	context = {

	}

	return  render(request, 'baseapp/atmosphere.html', context)

def show_about_us(request):

	context = {

	}

	return  render(request, 'baseapp/about_us.html', context)	

def show_contact_us(request):

	context = {

	}

	return  render(request, 'baseapp/contact_us.html', context)

def show_cart(request):

	context = {

	}

	return  render(request, 'baseapp/cart.html', context)

def show_wishlist(request):

	context = {

	}

	return  render(request, 'baseapp/wishlist.html', context)

def show_lk(request):

	context = {

	}

	return  render(request, 'baseapp/lk.html', context)			
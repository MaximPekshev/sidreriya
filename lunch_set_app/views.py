from django.shortcuts import render
from django.views.generic import View

class LunchSetView(View):

    def get(self, request):
        return  render(request, 'lunch_set_app/lunch_set.html')
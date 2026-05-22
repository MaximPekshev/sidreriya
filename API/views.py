from django.shortcuts import render
from rest_framework import generics

from lunch_set_app.models import LunchSet
from lunch_set_app.serializers import LunchSetSerializer


class LunchSetList(generics.ListAPIView):
    serializer_class = LunchSetSerializer
    queryset = LunchSet.objects.prefetch_related(
        'objectforsetlunch_set__dish',
        'objectforsetlunch_set__dish_type'
    ).order_by('-date')


class LunchSetDetail(generics.RetrieveAPIView):
    serializer_class = LunchSetSerializer
    queryset = LunchSet.objects.prefetch_related(
        'objectforsetlunch_set__dish',
        'objectforsetlunch_set__dish_type'
    )
    lookup_field = 'date'

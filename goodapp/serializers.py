from rest_framework import serializers
from .models import Good

class GoodSerializer(serializers.ModelSerializer):

    class Meta:
    	model = Good
    	fields = ('pk','name', 'name_en', 'good_uid', 'price')
    		
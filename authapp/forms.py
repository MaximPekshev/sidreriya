from django import forms
 
class BuyerSaveForm(forms.Form):

	input_first_name  	= forms.CharField(max_length = 30, required=False)
	input_second_name  	= forms.CharField(max_length = 30, required=False)
	input_phone  		= forms.CharField(max_length = 20, required=False)
	input_locality  	= forms.CharField(max_length = 40, required=False)
	input_street  		= forms.CharField(max_length = 30, required=False)
	input_house  		= forms.CharField(max_length = 15, required=False)
	input_apartments  	= forms.CharField(max_length = 15, required=False)
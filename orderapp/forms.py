from django import forms
 
class OrderCreateForm(forms.Form):
    orderType = forms.CharField(max_length = 1)
    input_qty = forms.IntegerField(max_value=100, min_value=1, required=False)
    input_comment = forms.CharField(max_length = 2560, required=False)
    input_name = forms.CharField(max_length = 50, required=False)
    input_last_name = forms.CharField(max_length = 50, required=False)
    input_phone = forms.CharField(max_length = 50, required=False)
    input_address = forms.CharField(max_length = 256, required=False)
    pickupType = forms.CharField(max_length = 1, required=False)
    cookTimeType = forms.CharField(max_length = 1, required=False)
    inputTime = forms.TimeField(required=False)
    good_slug = forms.CharField(max_length = 50, required=False)
    input_email = forms.CharField(max_length = 100, required=False)
    order_items_list = forms.CharField(widget=forms.Textarea, required=False)

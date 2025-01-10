from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import View
from django.shortcuts import (
	render, 
	redirect
)
from django.urls import (
	reverse, 
	reverse_lazy
)
# from django.http import HttpResponse
from allauth.account.views import (
	PasswordChangeView, 
	PasswordResetView,
	PasswordResetDoneView,
	PasswordResetFromKeyView,
	LoginView,
	SignupView
)
from allauth.account.utils import (
    passthrough_next_redirect_url,
	get_request_param
)

from authapp.models import Buyer
from .forms import BuyerSaveForm

class ProfileView(View):
	def get(self, request):
		if request.user.is_authenticated:
			return render(request, 'authapp/profile.html')
		else:
			return render(request, 'authapp/non_auth_profile.html')
		
	def post(self, request):
		try:
			buyer = Buyer.objects.get(user=request.user)
		except Buyer.DoesNotExist:
			buyer = Buyer.objects.create(user=request.user)
		buyer_form = BuyerSaveForm(request.POST)
		if buyer_form.is_valid():
			buyer.first_name 	= buyer_form.cleaned_data['input_first_name']
			buyer.last_name 	= buyer_form.cleaned_data['input_second_name']
			buyer.phone 		= buyer_form.cleaned_data['input_phone']
			buyer.locality 		= buyer_form.cleaned_data['input_locality']
			buyer.street 		= buyer_form.cleaned_data['input_street']
			buyer.house 		= buyer_form.cleaned_data['input_house']
			buyer.apartments 	= buyer_form.cleaned_data['input_apartments']
			buyer.porch 		= buyer_form.cleaned_data['input_porch']
			buyer.floor 		= buyer_form.cleaned_data['input_floor']
			buyer.save()
		return redirect(request.META['HTTP_REFERER'])	


class CustomPasswordResetFromKeyView(PasswordResetFromKeyView):

	def get_context_data(self, **kwargs):
		ret = super(PasswordResetFromKeyView, self).get_context_data(**kwargs)
		ret['action_url'] = reverse('account_reset_password_from_key',kwargs={'uidb36': self.kwargs['uidb36'],'key': self.kwargs['key']})

		return ret

class CustomPasswordResetDoneView(PasswordResetDoneView):
	
	def get_context_data(self, **kwargs):
		ret = super(PasswordResetDoneView, self).get_context_data(**kwargs)
		return ret
		
class  CustomPasswordResetView(PasswordResetView):

	def get_context_data(self, **kwargs):
		ret = super(PasswordResetView, self).get_context_data(**kwargs)
		login_url = passthrough_next_redirect_url(self.request,reverse("account_login"),self.redirect_field_name)
		ret['password_reset_form'] = ret.get('form')

		ret.update({
			'login_url': login_url,
			})

		return ret
	
class CustomSignupView(SignupView):

	def get_context_data(self, **kwargs):
		ret = super(SignupView, self).get_context_data(**kwargs)
		form = ret['form']
		email = self.request.session.get('account_verified_email')
		if email:
			email_keys = ['email']
			if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
				email_keys.append('email2')
			for email_key in email_keys:
				form.fields[email_key].initial = email

		login_url = passthrough_next_redirect_url(self.request,reverse("account_login"),self.redirect_field_name)
		redirect_field_name = self.redirect_field_name
		redirect_field_value = get_request_param(self.request,redirect_field_name)

		ret.update({
			'login_url': login_url,
			'redirect_field_name': redirect_field_name,
			'redirect_field_value': redirect_field_value,
	    })
		return ret

class CustomLoginView(LoginView):
	def get_context_data(self, **kwargs):

		ret = super(LoginView, self).get_context_data(**kwargs)
		signup_url = passthrough_next_redirect_url(self.request,reverse('account_signup'),self.redirect_field_name)
		redirect_field_value = get_request_param(self.request,self.redirect_field_name)
		site = get_current_site(self.request)
		ret.update({
			'signup_url': signup_url,
			'site': site,
			'redirect_field_name': self.redirect_field_name,
			'redirect_field_value': redirect_field_value,
        })

		return ret

class CustomPasswordChangeView(PasswordChangeView):

    success_url = reverse_lazy('account_password_change_succes')
    def get_context_data(self, **kwargs):
        ret = super(PasswordChangeView, self).get_context_data(**kwargs)
        ret['password_change_form'] = ret.get('form')
        return ret

def account_password_change_succes(request):
	return render(request, 'authapp/change_password_succes.html')

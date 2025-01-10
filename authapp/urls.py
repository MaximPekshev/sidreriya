from django.urls import path
from django.urls import include
from authapp.views import (
    CustomPasswordChangeView,
    CustomLoginView,
    CustomSignupView,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetFromKeyView,
    ProfileView,
    account_password_change_succes, 
)

urlpatterns = [
	path('profile/save/', ProfileView.as_view(), name='profile_save'),
	path('profile/', ProfileView.as_view(), name='show_profile'),
	path('login/', CustomLoginView.as_view(), name='account_login'),
	path('signup/', CustomSignupView.as_view(), name='account_signup'),
	path('password/reset/key/', CustomPasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
	path('password/reset/done/', CustomPasswordResetDoneView.as_view(), name='account_reset_password_done'),
	path('password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
	path('password/change/success/', account_password_change_succes, name='account_password_change_succes'),
	path('password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
	path(''	, include('allauth.urls')),

]

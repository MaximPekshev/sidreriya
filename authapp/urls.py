from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
	
	path('login/', views.LoginView.as_view(), name="account_login"),
	path('signup/', views.SignupView.as_view(), name="account_signup"),
	path(''     , include('account.urls')),

]


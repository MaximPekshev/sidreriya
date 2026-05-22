from django.urls import path    
from API.views import (
    LunchSetList,
    LunchSetDetail
)

app_name = "API"

urlpatterns = [
    path('lunch-set/', LunchSetList.as_view()),
    path('lunch-set/<str:date>/', LunchSetDetail.as_view()),
]
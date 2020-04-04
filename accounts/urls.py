from django.urls import path

from . import views


app_name='accounts'

urlpatterns = [
    path('sign-up/', views.SignUp.as_view(), name='sign-up')
]
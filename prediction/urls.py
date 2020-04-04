from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'prediction'
urlpatterns = [
    path('', views.HealthCenterStatusList.as_view(), name='current_status'),
    path('status_create', views.HealthCenterStatusCreate.as_view(), name='status_create'),
    path('<int:pk>/status_delete', views.delete, name='status_delete')
]

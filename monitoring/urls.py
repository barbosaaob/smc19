from django.urls import path

from . import views

app_name = 'monitoring'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('mapa/', views.Map.as_view(), name='map'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    # Profile
    path('pacientes/<int:pk>/', views.ProfileDetail.as_view(), name='profile-detail'),
    path('pacientes/cadastrar/', views.ProfileCreate.as_view(), name='profile-create'),
    path('pacientes/<int:pk>/editar/', views.ProfileUpdate.as_view(), name='profile-update'),
    path('pacientes/<int:pk>/remover/', views.ProfileDelete.as_view(), name='profile-delete'),
    # Address
    path('pacientes/<int:profile>/enderecos/cadastrar/', views.AddressCreate.as_view(), name='address-create'),
    path('pacientes/<int:profile>/enderecos/<int:pk>/editar/', views.AddressUpdate.as_view(), name='address-update'),
    path('pacientes/<int:profile>/enderecos/<int:pk>/remover/', views.AddressDelete.as_view(), name='address-delete'),
    # Trip
    path('pacientes/<int:profile>/viagens/cadastrar/', views.TripCreate.as_view(), name='trip-create'),
    path('pacientes/<int:profile>/enderecos/<int:pk>/editar/', views.TripUpdate.as_view(), name='trip-update'),
    path('pacientes/<int:profile>/viagens/<int:pk>/remover/', views.TripDelete.as_view(), name='trip-delete'),
    # Monitoring
    path('atendimentos/<int:pk>/', views.MonitoringDetail.as_view(), name='monitoring-detail'),
    path('atendimentos/cadastrar/', views.MonitoringCreate.as_view(), name='monitoring-create'),
    path('atendimentos/<int:pk>/editar/', views.MonitoringUpdate.as_view(), name='monitoring-update'),
    path('atendimentos/<int:pk>/remover/', views.MonitoringDelete.as_view(), name='monitoring-delete'),
    #Request
    path('request/', views.RequestIndex.as_view(), name='request'),
    path('request/cadastrar/', views.RequestCreate.as_view(), name='request-create'),
    path('request/<int:pk>/remover/', views.RequestDelete.as_view(), name='request-delete'),
]

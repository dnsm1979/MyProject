from django.urls import path

from cards import views

app_name = 'cards'

urlpatterns = [
    path('add_lpu/', views.LPUCreateView.as_view(), name='add_lpu'),
    path('add_hardware/', views.AddHardwareView.as_view(), name='add_hardware'),
    path('add-city/', views.add_city_ajax, name='add_city_ajax'),
    path('add-country/', views.add_country_ajax, name='add_country_ajax'),
    path('add-region/', views.add_region_ajax, name='add_region_ajax'),
    path('api/get-devices-by-lpu/', views.get_devices_by_lpu, name='get_devices_by_lpu'),
    path('api/get-lpu-options/', views.get_lpu_options, name='get_lpu_options'),
    
]
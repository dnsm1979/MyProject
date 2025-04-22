from django.urls import path

from cards import views

app_name = 'cards'

urlpatterns = [
    path('add_lpu/', views.AddLPUView.as_view(), name='add_lpu'),
    path('add_hardware/', views.AddHardwareView.as_view(), name='add_hardware'),
    
]
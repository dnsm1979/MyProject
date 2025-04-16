from django.urls import path

from image_manager import views

app_name = 'image_manager'

urlpatterns = [
    path('uppload_images/', views.AddLocationPageView.as_view(), name='uppload_images'),

]
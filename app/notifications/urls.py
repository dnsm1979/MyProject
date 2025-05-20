from django.urls import path
from .views import CreateNotificationView, NotificationCountView

app_name = 'notifications'

urlpatterns = [
    path('create_notification/<int:pk>', CreateNotificationView.as_view(), name='create_notification'),
    path('count/', NotificationCountView.as_view(), name='notification_count'),
]
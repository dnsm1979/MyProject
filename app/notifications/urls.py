from django.urls import path
from .views import CreateNotificationView, NotificationCountView, DeleteNotificationView, ClearAllNotificationsView, MarkNotificationReadView

app_name = 'notifications'

urlpatterns = [
    path('create_notification/<int:pk>', CreateNotificationView.as_view(), name='create_notification'),
    path('count/', NotificationCountView.as_view(), name='notification_count'),
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='delete_notification'),
    path('clear-all/', ClearAllNotificationsView.as_view(), name='clear_all'),
    path('notifications/<int:pk>/mark-read/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
]
from .models import Notifications
from django.core.cache import cache

def notifications_context(request):
    context = {}
    if request.user.is_authenticated:
        # Получаем уведомления и счетчик
        notifications = Notifications.objects.filter(
            user=request.user
        ).order_by('-created')[:10]  # Последние 10 уведомлений
        
        unread_count = Notifications.objects.filter(
            user=request.user,
            read=False
        ).count()
        
        context.update({
            'notifications': notifications,
            'unread_notifications_count': unread_count,
            'has_unread_notifications': unread_count > 0,
        })
    return context
# def notification_count(request):
#     if request.user.is_authenticated:
#         return {
#             'unread_notifications_count': request.user.notifications.filter(read=False).count()
#         }
#     return {'unread_notifications_count': 0}
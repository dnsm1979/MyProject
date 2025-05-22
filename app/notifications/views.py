from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from act_technical.models import ActT, CommentsActT
from .models import Notifications


class CreateNotificationView(LoginRequiredMixin, View):
    """Оптимизированный view для создания уведомлений"""
    
    # Отключаем CSRF для API-запросов (если нужно)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, act_id):
        # Быстрая проверка прав
        if not request.user.has_perm('notifications.add_notifications'):
            raise PermissionDenied("У вас нет прав на создание уведомлений")
        
        # Используем select_related для оптимизации запроса
        act = get_object_or_404(
            ActT.objects.select_related('user'),
            id=act_id
        )
        
        last_comment = CommentsActT.objects.filter(act=act).order_by('-created_at').first()

        # Используем bulk_create если нужно создавать много уведомлений
        notification = Notifications.objects.create(
            user=act.user,
            text=last_comment.text if last_comment else "Новый комментарий",
            name=act.name[:255],  # Ограничение на случай длинных имен
            absolute_url=self._get_absolute_url(act),
            read=False
        )
        
        return JsonResponse({
            'status': 'success',
            'notification_id': notification.id,
            'created_at': notification.created_at.isoformat() if hasattr(notification, 'created_at') else None
        })
    
    def _get_absolute_url(self, act):
        """Получение URL с кешированием"""
        # Можно добавить кеширование, если URL часто запрашивается
        return reverse('act_technical:act_change', kwargs={'pk': act.id})


class NotificationCountView(LoginRequiredMixin, View):
    def get(self, request):
        count = request.user.notifications.filter(read=False).count()
        return JsonResponse({'unread_count': count})
    

class DeleteNotificationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            notification = request.user.notifications.get(pk=pk)
            notification.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class ClearAllNotificationsView(LoginRequiredMixin, View):
    def post(self, request):
        deleted_count, _ = Notifications.objects.filter(user=request.user).delete()
        return JsonResponse({
            'status': 'success',
            'deleted_count': deleted_count
        })
    
class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            notification = request.user.notifications.get(pk=pk)
            notification.read = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
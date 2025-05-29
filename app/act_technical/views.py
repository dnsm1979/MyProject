
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from notifications.models import Notifications
from notifications.views import CreateNotCommRepView, CreateNotificationView
from .forms import ActAddForm, ActImageForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CardHardware, CardLPU, ActT, User, CommentsActT, ActImage

from django.template.loader import get_template
from xhtml2pdf import pisa
import os
import json
import pdfkit
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods




class ActAddView(LoginRequiredMixin, CreateView):
    template_name = 'act_technical/act_add.html'
    model = ActT
    form_class = ActAddForm

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not kwargs.get('instance'):
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.generate_act_name()
        if not form.instance.user:
            form.instance.user = self.request.user
        
        response = super().form_valid(form)
        
        # Проверяем, какая кнопка была нажата
        if 'save_and_new' in self.request.POST:
            return redirect(reverse('act_technical:act_add'))  # Перенаправляем на страницу создания нового акта
        return response
    
    def get_success_url(self):
        return reverse('act_technical:act_change', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового акта технического состояния'
        context['order'] = True


        context['device'] = CardHardware.objects.all()
        context['lpu'] = CardLPU.objects.all()
        return context
    






class ActChangeView(LoginRequiredMixin, DetailView):
    template_name = 'act_technical/act_change.html'
    model = ActT
    context_object_name = 'actt'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        act = self.object
        context['leader'] = User.objects.filter(position='руководитель').first()
        context['comments'] = CommentsActT.objects.filter(act=act).order_by('-created_at')
        context['images'] = ActImage.objects.filter(act=act).order_by('-uploaded_at')
        return context
    

def upload_act_image(request, pk):
    if request.method == 'POST':
        act = ActT.objects.get(pk=pk)
        file = request.FILES.get('image')
        
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        image = ActImage(act=act, image=file)
        image.save()
        
        return JsonResponse({
            'id': image.id,
            'url': image.image.url,
            'name': image.image.name.split('/')[-1]
        }, status=201)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_http_methods(["DELETE"])
def delete_act_image(request, pk):
    try:
        image = ActImage.objects.get(pk=pk)
        image_url = image.image.url  # Сохраняем URL перед удалением
        image.delete()
        return JsonResponse({
            'success': True,
            'message': 'Изображение успешно удалено',
            'deleted_id': pk,
            'image_url': image_url
        })
    except ActImage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Изображение не найдено'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)



class ActEditView(LoginRequiredMixin, UpdateView):
    template_name = 'act_technical/act_edit.html'
    model = ActT
    form_class = ActAddForm
    
    def get_success_url(self):
        return reverse('act_technical:act_change', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not kwargs.get('instance'):
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['user'] = self.request.user
            
        return kwargs

    def form_valid(self, form):
        form.instance.generate_act_name()
        # Убедимся, что пользователь установлен
        if not form.instance.user:
            form.instance.user = self.request.user


        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        act = self.object
        context['title'] = 'Редактирование акта технического состояния'
        context['order'] = True
        context['device'] = CardHardware.objects.all()
        context['lpu'] = CardLPU.objects.all()
        context['selected_lpu'] = self.object.lpu_id if self.object.lpu else None
        context['selected_device'] = self.object.device_id if self.object.device else None
        context['image_form'] = ActAddForm()
        context['images'] = self.object.images.all()
        context['comments'] = CommentsActT.objects.filter(act=act).order_by('-created_at')
        return context
    

class ActEdit2View(LoginRequiredMixin, UpdateView):
    template_name = 'act_technical/act_add.html'
    model = ActT
    form_class = ActAddForm
    success_url = reverse_lazy('main:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not kwargs.get('instance'):
            kwargs['initial'] = kwargs.get('initial', {})
            kwargs['initial']['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.generate_act_name()
        # Убедимся, что пользователь установлен
        if not form.instance.user:
            form.instance.user = self.request.user
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование акта технического состояния и сохранения как новый'
        context['order'] = True


        context['device'] = CardHardware.objects.all()
        context['lpu'] = CardLPU.objects.all()
        return context
    







def link_callback(uri, rel):
    """
    Преобразует URI статических файлов в абсолютные пути
    """
    # Обработка статических файлов
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(
            settings.STATIC_ROOT,
            uri.replace(settings.STATIC_URL, "", 1))
    # Обработка медиа файлов
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, "", 1))
    # Обработка абсолютных путей (например, для шрифтов)
    elif uri.startswith('http://') or uri.startswith('https://'):
        return uri  # Используем как есть
    else:
        # Для относительных путей (если нужно)
        return os.path.join(settings.STATIC_ROOT, uri)
    
    # Нормализация пути
    path = os.path.abspath(path)
    
    # Проверка существования файла
    if not os.path.exists(path):
        raise Exception(f"Static file not found: {path}")
    
    return path

def export_act_pdf(request, pk):
    act = get_object_or_404(ActT, pk=pk)
    leader = User.objects.filter(position='руководитель').first()
    
    context = {
        'actt': act,
        'leader': leader,
    }
    
    template = get_template('act_technical/act_pdf.html')
    html = template.render(context)

    options = {
          'page-size': 'A4',
          'encoding': "UTF-8",
          'enable-local-file-access': '',
       }
    try:
    # Пробуем использовать wkhtmltopdf из PATH
        config = pdfkit.configuration()
    except OSError:
    # Если не найден, указываем альтернативный путь
        config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    )


    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{act.name}.pdf"'
    return response
    


@login_required
def add_comment_to_act(request, pk):
    act = get_object_or_404(ActT, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            CommentsActT.objects.create(
                act=act,
                user=request.user,
                text=comment_text,
                active=True
            )


            notification_view = CreateNotificationView()
            notification_view.request = request
            notification_view.post(request, act.id)

    return redirect('act_technical:act_change', pk=pk)

@require_POST
@login_required
def toggle_comment_active(request, comment_id):
    try:
        # Получаем комментарий и связанный акт за один запрос
        comment = CommentsActT.objects.select_related('act').get(
            id=comment_id,
            act__user=request.user  # Проверка прав на изменение
        )
        comment.active = not comment.active
        comment.save()
        
        # Создаем уведомление
        notification = Notifications.objects.create(
            user=comment.user,  # Автор комментария получает уведомление
            name=f"Изменение статуса комментария в акте {comment.act.name}",
            text=f"Комментарий отмечен как {'Выполнен!' if not comment.active else 'активный'}",
            absolute_url=f"{reverse('act_technical:act_change', args=[comment.act.id])}#comment-{comment.id}",
            read=False
        )
        
        return JsonResponse({
            'success': True,
            'active': comment.active,
            'comment_id': comment_id,
            'notification_id': notification.id
        })
    except CommentsActT.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Комментарий не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)





# def toggle_comment_active(request, comment_id):
#     try:
#         comment = CommentsActT.objects.select_related('act').get(
#             id=comment_id, 
#             act__user=request.user  # Проверка, что пользователь - автор акта
#         )
#         comment.active = not comment.active
#         comment.save()
        
#         notification_view = CreateNotCommRepView()
#         notification_view.request = request
#         notification_view.post(request, comment)


#         return JsonResponse({
#             'success': True,
#             'active': comment.active,
#             'comment_id': comment_id
#         })
#     except CommentsActT.DoesNotExist:
#         return JsonResponse({'success': False}, status=404)
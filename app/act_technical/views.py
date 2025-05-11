
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from .forms import ActAddForm, ActImageForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CardHardware, CardLPU, ActT, User, CommentsActT, ActImage

from django.template.loader import get_template
from xhtml2pdf import pisa
import os
import json
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
        context['title'] = 'Редактирование акта технического состояния'
        context['order'] = True
        context['device'] = CardHardware.objects.all()
        context['lpu'] = CardLPU.objects.all()
        context['selected_lpu'] = self.object.lpu_id if self.object.lpu else None
        context['selected_device'] = self.object.device_id if self.object.device else None
        context['image_form'] = ActAddForm()
        context['images'] = self.object.images.all()
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
    





# class ActUpdateView(LoginRequiredMixin, UpdateView):
#     model = ActT
#     template_name = 'act_technical/act_edit.html'
#     form_class = UploadImagesForm

#     def get_success_url(self):
#         # Возвращаем URL текущего акта вместо главной страницы
#         return reverse_lazy('act_technical:act_change', kwargs={'pk': self.object.pk})

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['image_form'] = UploadImagesForm()
#         context['images'] = self.object.images.all()
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         image_form = UploadImagesForm(request.POST, request.FILES)
        
#         if 'images' in request.FILES:
#             files = request.FILES.getlist('images')
#             for file in files:
#                 ActImage.objects.create(
#                     act=self.object,
#                     image=file,
#                     description=request.POST.get('description', '')
#                 )
#             messages.success(request, 'Изображения успешно загружены')
#             return redirect(self.get_success_url())
        
#         messages.error(request, 'Ошибка загрузки изображений')
#         return self.form_invalid(form)



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
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="act_{act.id}.pdf"'
    
    # Генерация PDF с обработкой ошибок
    try:
        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            encoding='UTF-8',
            link_callback=link_callback
        )
        
        if pisa_status.err:
            return HttpResponse(f"Ошибка генерации PDF: {pisa_status.err}", status=400)
            
    except Exception as e:
        return HttpResponse(f"Ошибка: {str(e)}", status=500)
    
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

    return redirect('act_technical:act_change', pk=pk)
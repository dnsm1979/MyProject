from pyexpat.errors import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from act_technical.forms import ActAddForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import CardHardware, CardLPU, ActT, User, CommentsActT
from django.template.loader import render_to_string
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from io import BytesIO



class ActAddView(LoginRequiredMixin, CreateView):
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
        return context
    


class ActEditView(LoginRequiredMixin, UpdateView):
    template_name = 'act_technical/act_edit.html'
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
        context['title'] = 'Редактирование акта технического состояния'
        context['order'] = True
        context['device'] = CardHardware.objects.all()
        context['lpu'] = CardLPU.objects.all()
        context['selected_lpu'] = self.object.lpu_id if self.object.lpu else None
        context['selected_device'] = self.object.device_id if self.object.device else None
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



# @login_required
# def add_comment_to_act(request, pk):
#     act = get_object_or_404(ActT, pk=pk)
#     if request.method == 'POST':
#         comment_text = request.POST.get('comment', '').strip()
#         if comment_text:
#             CommentsActT.objects.create(
#                 act=act,
#                 user=request.user,
#                 text=comment_text,
#                 active=True
#             )
#             messages.success(request, 'Комментарий успешно сохранен')
#         else:
#             messages.error(request, 'Комментарий не может быть пустым')
#     return redirect('act_technical/act_change', pk=pk)


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
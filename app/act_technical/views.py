from pyexpat.errors import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from act_technical.forms import ActAddForm
from .models import CardHardware, CardLPU, ActT


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

        act = self.object
        


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
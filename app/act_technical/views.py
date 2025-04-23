from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from act_technical.forms import ActAddForm

from .models import CardHardware, CardLPU


class ActAddView(LoginRequiredMixin, FormView):
    template_name = 'act_technical/act_add.html'
    form_class = ActAddForm
    success_url = reverse_lazy('main:index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание нового акта технического состояния'
        context['order'] = True


        context['device'] = CardHardware.objects.all()
        context['lpu'] = CardLPU.objects.all()
        return context

# class ActAddView(TemplateView):
#     template_name = 'act_technical/act_add.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


class ActChangeView(TemplateView):
    template_name = 'act_technical/act_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

class ActEditView(TemplateView):
    template_name = 'act_technical/act_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
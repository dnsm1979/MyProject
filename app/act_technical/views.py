from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView




class ActAddView(TemplateView):
    template_name = 'act_technical/act_add.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
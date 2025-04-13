from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView




class AddHardwareView(TemplateView):
    template_name = 'cards/add_card_hardware.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddLpuView(TemplateView):
    template_name = 'cards/add_card_lpu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

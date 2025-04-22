from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView


from cards.forms import AddHardwareForm, AddLPUForm

from .models import Country



# class AddHardwareView(TemplateView):
#     template_name = 'cards/add_card_hardware.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


# class AddLpuView(TemplateView):
#     template_name = 'cards/add_card_lpu.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
    
class AddHardwareView(LoginRequiredMixin, FormView):
    template_name = 'cards/add_card_hardware.html'
    form_class = AddHardwareForm
    success_url = reverse_lazy('act_technical:act_add')

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['name'] = self.request.user.name
    #     initial['model'] = self.request.user.model
    #     initial['serial_number'] = self.request.user.serial_number
    #     initial['invent_number'] = self.request.user.invent_number
    #     initial['year_of_manufacture'] = self.request.user.year_of_manufacture
    #     initial['year_of_sale'] = self.request.user.year_of_sale
    #     initial['commissioning_date'] = self.request.user.commissioning_date
    #     initial['lpu'] = self.request.user.lpu
    #     initial['cauntry'] = self.request.user.cauntry
    #     return initial

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление оборудования'
        context['order'] = True
        context['countries'] = Country.objects.all()
        return context
    

class AddLPUView(LoginRequiredMixin, FormView):
    template_name = 'cards/add_card_lpu.html'
    form_class = AddLPUForm
    success_url = reverse_lazy('act_technical:act_add')

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['name'] = self.request.user.name
    #     initial['adress'] = self.request.user.adress
    #     initial['index'] = self.request.user.index
    #     initial['zip'] = self.request.user.zip
    #     initial['representative_1'] = self.request.user.representative_1
    #     initial['representative_2'] = self.request.user.representative_2
    #     initial['representative_3'] = self.request.user.representative_3
    #     initial['lpu'] = self.request.user.lpu
    #     initial['city'] = self.request.user.city
    #     return initial

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление ЛПУ'
        context['order'] = True
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView


from cards.forms import AddHardwareForm, AddLPUForm

from cards.models import CardHardware, CardLPU
from main.models import Country, City, Region



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
    
class AddHardwareView(LoginRequiredMixin, CreateView):
    template_name = 'cards/add_card_hardware.html'
    model = CardHardware
    fields = '__all__'
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
        context['country'] = Country.objects.all()
        context['manufacturer_name'] = CardHardware.objects.values_list('manufacturer', flat=True).distinct()
        context['model_names'] = CardHardware.objects.values_list('model', flat=True).distinct()
        context['lpu'] = CardLPU.objects.all()
        context['existing_names'] = CardHardware.objects.values_list('name', flat=True).distinct()
        return context
    

class LPUCreateView(LoginRequiredMixin, CreateView):
    template_name = 'cards/add_card_lpu.html'
    model = CardLPU
    fields = '__all__'
    success_url = reverse_lazy('act_technical:act_add')






    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['name'] = self.request.cards.name

    #     return initial

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление ЛПУ'
        context['order'] = True
        context['city'] = City.objects.all()
        context['zip_name'] = Region.objects.all()
        return context
    

def add_city_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            city = City.objects.create(city=name)
            return JsonResponse({
                'id': city.id,
                'name': city.city
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_country_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            country = Country.objects.create(country=name)
            return JsonResponse({
                'id': country.id,
                'name': country.country
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import JsonResponse


def add_region_ajax(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            zip = Region.objects.create(zip=name)
            return JsonResponse({'id': zip.id, 'name': zip.zip})
    return JsonResponse({'error': 'Invalid request'}, status=400)





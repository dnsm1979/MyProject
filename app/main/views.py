from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from act_technical.models import ActT
from django.db.models import Q

from cards.models import CardLPU
from users.models import User




class IndexView(LoginRequiredMixin, ListView):
    template_name = 'main/index.html'
    model = ActT
    context_object_name = 'acts'
    paginate_by = 10
    ordering = ['-creation_date']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('lpu', 'device', 'user')
        
        # Получаем параметры фильтрации
        params = self.request.GET
        
        # Фильтрация по поиску
        if q := params.get('q'):
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(lpu__name__icontains=q) |
                Q(device__model__icontains=q)
            )
        
        # Фильтрация по ЛПУ
        if lpu_id := params.get('lpu'):
            queryset = queryset.filter(lpu_id=lpu_id)
        
        # Фильтрация по создателю
        if creator_id := params.get('creator'):
            queryset = queryset.filter(user_id=creator_id)
        
        # Фильтрация по дате
        if date_from := params.get('date_from'):
            queryset = queryset.filter(creation_date__gte=date_from)
        if date_to := params.get('date_to'):
            queryset = queryset.filter(creation_date__lte=date_to)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем данные для фильтров
        context['all_lpus'] = CardLPU.objects.all()
        context['all_creators'] = User.objects.filter(actt__isnull=False).distinct()
        context['current_filters'] = self.request.GET
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
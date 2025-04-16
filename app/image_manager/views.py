
from django.views.generic.edit import FormView
from .models import Location, Photo
from .forms import LocationForm
from django.urls import reverse_lazy



class AddLocationPageView(FormView):
    template_name = 'uppload_images.html'
    form_class = LocationForm
    success_url = reverse_lazy('act_technical:act_change')  # путь для перенаправления после успешной загрузки

    def form_valid(self, form):
        # Сохраняем новую локацию
        location = form.save(commit=False)
        location.user = self.request.user
        location.save()
        
        # Обрабатываем каждое изображение и сохраняем его
        for image in self.request.FILES.getlist('images'):
            Photo.objects.create(location=location, image=image)
        
        return super().form_valid(form)
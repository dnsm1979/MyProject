from django.db import models

from django.conf import settings

class Location(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Локация", default='')
    
class Photo(models.Model):
    location = models.ForeignKey(Location, related_name="photos", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
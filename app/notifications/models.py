from django.db import models

from users.models import User

class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    name = models.CharField(max_length=255)
    absolute_url = models.CharField(max_length=512)
    text = models.CharField(max_length=512)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

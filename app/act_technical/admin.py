from django.contrib import admin

from act_technical.models import ActT, CommentsActT, ActImage


admin.site.register(ActT)
admin.site.register(CommentsActT)
admin.site.register(ActImage)
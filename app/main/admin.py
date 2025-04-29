from django.contrib import admin

from main.models import Country, City, Templates, Region


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Templates)
admin.site.register(Region)

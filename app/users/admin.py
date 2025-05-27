from django.contrib import admin
# from carts.admin import CartTabAdmin
# from orders.admin import OrderTabulareAdmin

from users.models import User, UserCategory

admin.site.register(UserCategory)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "surname", "position", "email", "phone_number",]
    search_fields = ["username", "first_name", "last_name", "surname", "position", "email", "phone_number",]

    

    # inlines = [CartTabAdmin, OrderTabulareAdmin]
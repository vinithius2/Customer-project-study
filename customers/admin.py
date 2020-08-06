from django.contrib import admin
from customers.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "gender", "email", "city"]


admin.site.register(Customer, CustomerAdmin)

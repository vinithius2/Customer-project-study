from django.contrib import admin
from customers.models import Customer, City


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "gender", "email", "company", "title", "city"]


class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "latitude", "longitude"]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(City, CityAdmin)

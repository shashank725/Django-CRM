from django.contrib import admin
from .models import Customer, Product, Order, Tag

# Register your models here.

@admin.register(Customer)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email', 'date_created']

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)
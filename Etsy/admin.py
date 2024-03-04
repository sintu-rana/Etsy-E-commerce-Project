from django.contrib import admin
from Etsy.models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)

# admin.site.register(customuser)
# admin.site.register(admin)
# admin.site.register(supplier)

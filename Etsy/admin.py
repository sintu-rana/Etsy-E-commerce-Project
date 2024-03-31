from django.contrib import admin
from Etsy.models import *
from Etsy.models.customer import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)

admin.site.register(CustomUser)
admin.site.register(Admin)
admin.site.register(Supplier)

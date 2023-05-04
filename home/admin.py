from django.contrib import admin 

from .models import *

admin.site.register(medicinecategory)
admin.site.register(medicines)
admin.site.register(Carts)
admin.site.register(CartItems)
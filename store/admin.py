from unicodedata import category
from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Category)
admin.site.register(Reviews)

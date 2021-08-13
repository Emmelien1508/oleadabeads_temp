from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Photo)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(Favorite)
admin.site.register(Discount)
admin.site.register(Review)
admin.site.register(Session)
admin.site.register(InventoryProduct)
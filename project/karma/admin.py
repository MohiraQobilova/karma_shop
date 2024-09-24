from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Brend)
admin.site.register(CartItem)
admin.site.register(OrderStatus)
admin.site.register(PaymentType)
admin.site.register(Order)
admin.site.register(Orderproduct)
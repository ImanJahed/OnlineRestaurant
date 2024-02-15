from django.contrib import admin

from .models import Order, OrderItem


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'order_placed_to', 'status', 'is_paid', 'created_at']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
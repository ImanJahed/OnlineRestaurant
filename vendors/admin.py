from django.contrib import admin

from .models import Vendor

# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_phone', 'get_email', 'is_approved']
    
    
    
    
    def get_phone(self, obj):
        return obj.user.phone_number
    
    def get_email(self, obj):
        return obj.user.email

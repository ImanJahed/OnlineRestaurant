from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import OTPCode, Profile, User
from .forms import CreateUserForm, EditUserForm
# Register your models here.

@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = EditUserForm
    add_form = CreateUserForm
    
    add_fieldsets = (
        (None, {'fields': ('phone_number', 'password1', 'password2')}),
    )
    
    fieldsets = (
        ('Information',{'fields':( 'password','phone_number', 'email', 'roll')}),
        
        ('Permission', {'fields':('is_active','is_staff','is_superuser')})
    )
    
    list_display = ['phone_number', 'email', 'roll', 'is_superuser']
    search_fields = ['phone_number']
    list_filter = ['roll', 'is_superuser']
    
    filter_horizontal = []
    ordering = 'phone_number',


admin.site.register(OTPCode)
admin.site.register(Profile)
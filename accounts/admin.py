from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class MyUserAdmin(UserAdmin):
    
    filter_vertical = []
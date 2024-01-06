from django.contrib import admin

from .models import Category, Food

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor']
    prepopulated_fields = {'slug': ['name']}


class FoodAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'category','vendor']
    prepopulated_fields = {'slug': ['food_name']}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Food, FoodAdmin)

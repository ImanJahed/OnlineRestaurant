from django.db import models

from vendors.models import Vendor


# Create your models here.

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='cat_vendor')
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
    def clean(self):
        self.name = self.name.title()    


def food_path_file(instance, filename):
    return f'restaurant_img/{instance.vendor.name}/{instance.category.name}/food/{filename}'

class Food(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='food_vendor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_cat')

    food_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    
    price = models.PositiveIntegerField()
    duration = models.PositiveSmallIntegerField()

    is_available = models.BooleanField(default=True)
    
    food_img = models.ImageField(upload_to=food_path_file)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.food_name
    
    def clean(self):
        self.food_name = self.food_name.title()
    

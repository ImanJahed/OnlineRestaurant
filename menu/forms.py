from typing import Any
from django import forms
from django.template.defaultfilters import slugify
from menu.models import Category, Food


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        
        super().__init__(*args, **kwargs)
        
        
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        instance.vendor = self.request.user.vendor_user
        slug = slugify(self.cleaned_data['name'])
        queryset = Category.objects.filter(slug=slug)
        if queryset.exists():
            slug = slugify(f"{self.cleaned_data['name']} - {queryset.count() + 1}")

        instance.slug = slug
        
        if commit:
            instance.save()
            
        return instance


class FoodForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Food.objects.none())
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(vendor__user=self.request.user)
        
        
    class Meta:
        model = Food
        fields = ("food_name", "category", "description", "price", "duration", "is_available", "food_img")

        widgets = {
            'food_img':forms.FileInput(attrs={'class': 'btn btn-info w-100'})
        }


        
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.vendor = self.request.user.vendor_user
        slug = slugify(self.cleaned_data['food_name'])
        queryset = Food.objects.filter(slug=slug)
        if queryset.exists():
            slug = slugify(f"{self.cleaned_data['food_name']} - {queryset.count() + 1}")

        instance.slug = slug

        if commit:
            instance.save()
        
        return instance
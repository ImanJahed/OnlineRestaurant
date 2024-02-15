from django import forms
from accounts.models import User

from order.models import Order


class OrderModelForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'city', 'state']
        
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Phone number already exists')
            
        return phone_number
    
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email Address already exists')
            
        return email
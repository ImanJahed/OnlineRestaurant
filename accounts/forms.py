import re
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import User
from vendors.models import Vendor
class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password Confirmation')

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password1', 'password2']
        
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Password Does not Match')
        
        return password1
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('Phone number already exist')
        
        return phone_number
    
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email address already exist')
        
        return email
    
    def save(self, commit: bool = True) -> Any:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            return user.save()
        
        return user


class EditUserForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField(help_text='You can change password with <a href="../password"/>This</a> link')
    
    class Meta:
        model = User
        fields = ['phone_number', 'email', 'password']
        
    
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        
        if User.objects.exclude(phone_number=self.id).filter(phone_number=phone_number).exists():
            raise ValidationError('Phone number already exist')
        
        return phone_number
    
    def clean_email(self):
        email = self.cleaned_data['phone_number']
        
        if User.objects.exclude(email=self.id).filter(email=email).exists():
            raise ValidationError('Phone number already exist')
        
        return email
    
    
def check_phone(phone):
    valid_phone = '09(0[0-9]|1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}'
    if not re.match(valid_phone, phone):
        raise ValidationError('Phone not Valid')
    return phone
class SendOtpCodeForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class':"foodbakery-dev-req-field"}), validators=[check_phone], max_length=11)



class VendorRegistrationForm(forms.ModelForm):
    
    class Meta:
        model = Vendor
        fields = ['name', 'license_file', 'profile_img', 'cover_img']
import re
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.template.defaultfilters import slugify
from accounts.models import Profile, User
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
        
        if User.objects.filter(phone_number=phone_number).exclude(pk=self.instance.id).exists():
            raise ValidationError('Phone number already exist')
        
        return phone_number
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        if User.objects.filter(email=email).exclude(pk=self.instance.id).exists():
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
        fields = ['name', 'license_file']
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'foodbakery-dev-req-field'}),
            'license_file': forms.FileInput(attrs={'class':'btn btn-info'}),
            'profile_img': forms.FileInput(attrs={'class':'btn btn-info'}),
            'cover_img': forms.FileInput(attrs={'class':'btn btn-info'}),
        }
    def save(self, commit: bool = True) -> Any:
        instance =  super().save(commit)
        slug = slugify(self.cleaned_data['name'])
        
        slug_query = Vendor.objects.filter(slug=slug)
        if slug_query.exists():
            slug = f'{slug}-{slug_query.count() + 1}'
        
        instance.slug = slug
        if commit:
            instance.save()
            
        return instance
        
class CustomerSetPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Password Does not match')
        
        return password1
    def __init__(self, user,*args, **kwargs):
        self.user = user
        return super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        
        if commit:
            self.user.save()
        return self.user
    
    
class CustomerEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ['user']
        
        widgets ={
            'img_cover': forms.FileInput(attrs={'class': 'btn btn-info'}),
            'img_profile': forms.FileInput(attrs={'class': 'btn btn-info'}),
        }


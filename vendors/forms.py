from django import forms
from accounts.models import Profile

from vendors.models import Vendor


class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = 'user',
        
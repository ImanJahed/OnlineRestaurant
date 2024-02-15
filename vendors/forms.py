from django import forms
from accounts.models import Profile

from vendors.models import Vendor, WorkingHours


class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = 'user',
        
        
class WorkingHoursForm(forms.ModelForm):
    
    class Meta:
        model = WorkingHours
        exclude = ['vendor']
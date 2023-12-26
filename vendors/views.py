from typing import Any
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from accounts.forms import VendorRegistrationForm
from django.contrib import messages
from utils import is_vendor, is_customer
from vendors.forms import EditProfileForm


# Create your views here.
class VendorProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'vendors/vendor_profile.html'

    def get(self, request):
        return render(request, self.template_name)
    
    
    def test_func(self):

        return is_vendor(self.request.user)
    
    

class VendorEditProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'vendors/v_edit_profile.html'
    form_class = VendorRegistrationForm
    form_class_p = EditProfileForm
    
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any):
        self.user = request.user.vendor_user
        self.user_p = request.user.profile
        return super().setup(request, *args, **kwargs)

    
    def get(self, request):
        form = self.form_class(instance=self.user)
        form_p = self.form_class_p(instance=self.user_p)
        context = {
            'form': form,
            'form_p': form_p
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, files=request.FILES, instance=self.user)
        form_p = self.form_class_p(request.POST, files=request.FILES, instance=self.user_p)

        if form.is_valid() and form_p.is_valid():
            form.save()
            form_p.save()
            messages.success(request, 'Profile Updated')
            return redirect('vendors:vendor_edit')
        
        context = {
            'form': form,
            'form_p': form_p
        }
        return render(request, self.template_name, context)
    
    def test_func(self):
        return is_vendor(self.request.user)
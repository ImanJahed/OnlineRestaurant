from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.views.generic import View
from django.utils import timezone
from django.contrib import messages

from vendors.models import Vendor
from . import authentications

from accounts.forms import CreateUserForm, SendOtpCodeForm, VendorRegistrationForm
from accounts.models import User ,OTPCode


# Create your views here.
class LogOutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('pages:home')
    
class SendOtp(View):
    template_name = 'accounts/send_otp_code.html'
    form_class = SendOtpCodeForm
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('pages:home')
        return super().dispatch(request, *args, **kwargs)
        
        
    def get(self, request):
        
        form = self.form_class()
        context = {
            'form': form
        }
        
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            otp = OTPCode()
            otp.generate_code()
            otp.phone_number = cd['phone_number']
            otp.save()
            
            request.session['user_session_info'] = {
                'otp_code': otp.code,
                'phone_number':cd['phone_number'],
                
            }
            # send SMS to user
            print(otp.code)
            return redirect('check_otp')
        return render(request, self.template_name, {'form': form})
    
    
    
class OTPCodeCheck(View):
    template_name = 'accounts/otp_code_check.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('pages:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        otp_code = request.POST.get('otp_code', None)
        phone_number = request.session['user_session_info']['phone_number']
        code = request.session['user_session_info']['otp_code']

        if otp_code:
            valid_code = get_object_or_404(OTPCode, phone_number=phone_number, code=code)

            if otp_code == valid_code.code and valid_code.expired_at >= timezone.now():
                
                user, is_created = User.objects.get_or_create(phone_number=phone_number)
                user.roll = 1
                user.save()
                
                login(request, user, backend='accounts.authentications.PhoneBackend')
                valid_code.delete()
                return redirect('pages:home')


            messages.error(request, 'Invalid Code')
            return render(request, self.template_name)

        messages.error(request, 'Enter Code')
        return redirect('check_otp')
    
    
class VendorRegister(View):
    template_name = 'accounts/vendor_registration.html'
    form_class = CreateUserForm
    form_class_v = VendorRegistrationForm
    
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form_user = self.form_class(request.POST)
        form_v = self.form_class_v(request.POST, files=request.FILES)
        
        if form_user.is_valid() and form_v.is_valid():
            cd = form_user.cleaned_data
            user = form_user.save(commit=False)
            vendor_user = form_v.save(commit=False)
            user.roll = 2
            user.save()
            user.profile.first_name = request.POST['first_name']
            user.profile.last_name = request.POST['last_name']
            user.profile.save()
            vendor_user.user = user
            vendor_user.vendor_profile = user.profile
            vendor_user.save()
            
            
        context = {
            'form_user': form_user,
            'form_v': form_v
        }
        return render(request, self.template_name, context)
    
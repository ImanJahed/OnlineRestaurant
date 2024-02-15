from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger
from datetime import datetime

from accounts.forms import CreateUserForm, CustomerEditForm, CustomerSetPasswordForm, EditUserForm, SendOtpCodeForm, VendorRegistrationForm
from accounts.models import User ,OTPCode
from order.models import Order, OrderItem
from utils import is_customer
from vendors.models import Vendor


# Create your views here.

class ProfileDispatcher(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.roll == 1:
            return redirect('customer_profile')

        elif request.user.roll == 2:
            return redirect('vendors:vendor_dashboard')

        elif request.user.roll is None and request.user.is_superuser:
            return redirect('admin_profile')

        return super().dispatch(request, *args, **kwargs)



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
                if user.roll is None:
                    user.roll = 1
                    user.save()
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
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect('vendor_register')

        context = {
            'form_user': form_user,
            'form_v': form_v
        }
        return render(request, self.template_name, context)



class CustomerProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'accounts/c_profile.html'

    def get(self, request):

        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        page_num = request.GET.get('page', 1)
        paginator = Paginator(orders, per_page=5)
        try:
            page_object = paginator.get_page(page_num)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            'orders':page_object,
        }
        return render(request, self.template_name, context)

    def test_func(self):
        return is_customer(self.request.user)




class CustomerEditProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'accounts/c_edit_profile.html'
    form_class = EditUserForm
    form_class_c = CustomerEditForm

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.user = request.user
        self.user_profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request):

        form = self.form_class(instance=self.user)
        form_c = self.form_class_c(instance=self.user_profile)

        context = {
            'form': form,
            'form_c': form_c
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, instance=self.user)
        form_c = self.form_class_c(request.POST, request.FILES, instance=self.user_profile)
        if form.is_valid() and form_c.is_valid():
            form.save()
            form_c.save()

            messages.success(request, 'Profile Updated')
            return redirect('edit_profile')
        context ={
            'form':form,
            'form_c': form_c
        }
        return render(request, self.template_name, context)
    def test_func(self):

        return is_customer(self.request.user)


class CustomerSetPassword(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'registration/password_change_form.html'
    form_class = CustomerSetPasswordForm

    def get(self, request):
        form = self.form_class(request.user)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.user, request.POST, )

        if form.is_valid():
            form.save(commit=False)
            password = form.cleaned_data['new_password1']
            user = authenticate(username=request.user.phone_number, password=password)
            form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'registration/password_change_done.html')

        return render(request, self.template_name, {'form': form})



    def test_func(self):
        return is_customer(self.request.user)




# -------------------------------- Admin Dashboard ----------------------------------------------
class AdminDashboardView(UserPassesTestMixin,LoginRequiredMixin,View):
    template_name = 'accounts/admin_profile.html'

    def get(self, request):
        orders = Order.objects.all()
        orders_count = orders.count()
        total_revenue = sum(order.total_price for order in orders)

        current_month = datetime.now().month
        this_month_order= orders.filter(created_at__month=current_month)
        current_month_revenue = sum(order.total_price for order in this_month_order)

        context = {
            'orders': orders,
            'orders_count': orders_count,
            'total_revenue': total_revenue,
            'current_month_revenue': current_month_revenue
        }
        return render(request, self.template_name, context)


    def test_func(self):
        return self.request.user.is_superuser



class AdminOrderDetailView(UserPassesTestMixin,LoginRequiredMixin,View):
    template_name = 'accounts/admin_order_detail.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order_item = OrderItem.objects.filter(order=order)
        total_shipment = sum(ord.shipment for ord in order.vendors.all())

        context = {
            'order':order,
            'order_item': order_item,
            'total_shipment':total_shipment,

        }

        return render(request, self.template_name, context)


    def test_func(self):
        return self.request.user.is_superuser



class AdminEarningsView(UserPassesTestMixin,LoginRequiredMixin,View):
    template_name = 'accounts/admin_earnings.html'

    def get(self, request):
        date_start = request.GET.get('date_start', None)
        date_end = request.GET.get('date_end', None)
        q_res = request.GET.get('res', None)

        today = datetime.today()

        orders = Order.objects.all()

        today_revenue = sum(order.total_price for order in orders)


        context = {
            'orders': orders,
            'revenue': today_revenue
        }


        if date_start:
            orders_start_date = orders.filter(created_at__date=date_start)
            revenue_start_date = sum(order.total_price for order in orders_start_date)
            context['orders'] = orders_start_date
            context['revenue'] = revenue_start_date

        if date_start and date_end:
            orders_start_end_time = orders.filter(created_at__lte=date_start, created_at__gte=date_end)
            revenue_start_end_time = sum(order.total_price for order in orders_start_end_time)

            context['orders'] = orders_start_end_time
            context['revenue'] = revenue_start_end_time

        if q_res:
            vendor = Vendor.objects.filter(name__icontains=q_res)

            orders_res = orders.filter(vendors__in=vendor)

            revenue_per_restaurant = sum(order.total_price for order in orders_res) * (10/100)

            context['orders'] = orders_res
            context['revenue'] = revenue_per_restaurant

        if date_start and date_end and q_res:
            vendor = Vendor.objects.filter(name__icontains=q_res)
            orders_res_and_date = orders.filter(created_at__lte=date_start, created_at__gte=date_end, vendors__in=vendor)

            revenue_per_restaurant_and_date = sum(order.total_price for order in orders_res_and_date) * (10/100)

            context['orders'] = orders_res_and_date
            context['revenue'] = revenue_per_restaurant_and_date



        return render(request, self.template_name, context)


    def test_func(self):
        return self.request.user.is_superuser

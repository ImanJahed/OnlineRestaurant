import datetime
import json
from typing import Any
from django.db import IntegrityError
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from accounts.forms import VendorRegistrationForm
from marketplace.cart import Cart
from order.models import Order, OrderItem
from utils import is_vendor, is_customer
from vendors.forms import EditProfileForm, WorkingHoursForm
from vendors.models import Vendor, WorkingHours


# Create your views here.
class VendorProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'vendors/vendor_profile.html'

    def get(self, request):

        vendor = Vendor.objects.get(user=request.user)
        orders = Order.objects.filter(vendors=vendor).order_by('-created_at')
        orders_count = orders.count()

        total_revenue = sum([json.loads(item.vendor_share)[str(vendor.id)] for item in orders if item.vendor_share is not None and str(vendor.id) in json.loads(item.vendor_share)])

        current_month = datetime.datetime.now().month
        current_month_order = orders.filter(created_at__month=current_month, vendors=vendor)
        current_month_revenue= sum([json.loads(item.vendor_share)[str(vendor.id)] for item in current_month_order if item.vendor_share is not None and str(vendor.id) in json.loads(item.vendor_share)])


        context ={
            "orders": orders,
            'orders_count':orders_count,
            'total_revenue':total_revenue,
            'current_month_revenue': current_month_revenue

        }
        return render(request, self.template_name, context)


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


#----------------- Working Hours CRUD  -------------------


class WorkingHoursView(UserPassesTestMixin, LoginRequiredMixin, View):
    template_name = 'vendors/working_hours.html'
    form_class = WorkingHoursForm

    def get(self,request):
        form = self.form_class()
        working_hours = WorkingHours.objects.filter(vendor=request.user.vendor_user)

        context = {
            'working_hours':working_hours,
            'form':form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        view = CreateWorkingHours
        return view.as_view()

    def delete(self, request):
        view = RemoveWorkingHourView
        return view.as_view()

    def test_func(self) -> bool:
        return is_vendor(self.request.user)


class CreateWorkingHours(LoginRequiredMixin, View):
    form_class = WorkingHoursForm

    def post(self, request):
        days = request.POST.get('days')
        from_hour = request.POST.get('from_hour')
        to_hour = request.POST.get('to_hour')
        is_closed = request.POST.get('is_closed')

        try:
            hour = WorkingHours.objects.create(vendor=request.user.vendor_user, days=days, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
            if hour:
                day = WorkingHours.objects.get(id=hour.id)
                if day.is_closed:
                    response = {'status': 'success', 'id': hour.id, 'days':day.get_days_display(),'is_closed': 'Closed'}
                else:
                    response = {'status': 'success', 'id': hour.id, 'days':day.get_days_display(), 'from_hour':from_hour, 'to_hour':to_hour}
            return JsonResponse(response)

        except IntegrityError as e:
            response = {'status':'failed', 'message': f'{from_hour} - {to_hour} already exists for this day!'}

            return JsonResponse(response)

class RemoveWorkingHourView(LoginRequiredMixin, View):

    def get(self,request, pk):
        hour = get_object_or_404(WorkingHours, pk=pk)
        hour.delete()
        return JsonResponse({'status':'success', 'id':pk})

# ---------------------------- END -----------------------------------
class VendorOrderView(View):
    template_name = 'vendors/my_order.html'

    def get(self, request):

        vendor = Vendor.objects.get(user=request.user)
        orders = Order.objects.filter(vendors=vendor).order_by('-created_at')

        context = {
            "vendor": vendor,
            "orders": orders
        }


        return render(request, self.template_name, context)
class VendorOrderDetailView(View):
    template_name = 'vendors/vendor_order_detail.html'

    def get(self, request, pk):
        order = Order.objects.get(id=pk, vendors=request.user.vendor_user)
        order_item = OrderItem.objects.filter(order=order, food__vendor=request.user.vendor_user)

        context = {
            'order': order,
            'order_item': order_item,


        }
        return render(request, self.template_name, context)

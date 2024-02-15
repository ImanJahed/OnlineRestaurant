import json
from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings
from django.contrib.auth import login

from accounts.models import Profile, User
from marketplace.cart import Cart
from menu.models import Food

from order.models import Order, OrderItem
from vendors.models import Vendor

from .forms import OrderModelForm

# Create your views here.




class CheckOutView(View):
    template_name = 'marketplace/checkout.html'
    form_class = OrderModelForm


    def get(self, request):
        form = self.form_class()
        cart = Cart(request)


        context = {
            "form": form,
            'cart': cart
        }
        return render(request, self.template_name, context)


    def post(self, request):
        form = self.form_class(request.POST)
        cart = Cart(request)

        food_ids = [item['id'] for item in cart]
        vendors = Vendor.objects.prefetch_related('food_vendor').filter(food_vendor__in=food_ids)
        vendor_ids = list(set(i for i  in vendors))

        if form.is_valid():
            print(10 * '*')
            vendor_data = {}
            tp = request.POST.get('total_price')
            ts = request.POST.get('total_shipment')

            cd = form.cleaned_data
            user = User.objects.create_user(phone_number=cd['phone_number'],email=cd['email'])
            user.roll = 1
            user.save()
            Profile.objects.filter(user=user).update(first_name=cd['first_name'], last_name=cd['last_name'], address=cd['address'],
                                   city=cd['city'], province=cd['state'])

            order = Order.objects.create(user=user,total_price=(tp),total_shipment=(ts), **form.cleaned_data)
            order.vendors.set(vendor_ids)

            order.admin_share = float(tp) * (10/100)

            for item in cart.cart.values():

                if item['vendor_id'] not in vendor_data:
                    vendor_data[item['vendor_id']] = item['total_item_price'] * (90/100)
                else:
                    vendor_data[item['vendor_id']] += item['total_item_price'] * (90/100)

            order.vendor_share = json.dumps(vendor_data)



            # order.add(vendors_id)
            order.save()
            for item in cart:
                food = Food.objects.get(id=item['id'])
                OrderItem.objects.create(order=order, food=food, quantity=item['quantity'], price=item['total_item_price'])


            if user:
                login(request, user,backend=settings.AUTHENTICATION_BACKENDS[1])
            return redirect('order_complete')

        return render(request, self.template_name, {'form': form})


class OrderCompleteView(View):
    template_name = 'order/order_complete.html'

    def get(self, request):
        order = Order.objects.get(user=request.user)
        order_item = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'order_item': order_item
        }
        return render(request, self.template_name, context)

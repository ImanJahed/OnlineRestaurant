from datetime import datetime
import json
from typing import Any
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View
from django.db.models import Prefetch

from menu.models import Category, Food


from vendors.models import Vendor, WorkingHours
from .cart import Cart

# Create your views here.


class VendorListView(ListView):
    model = Vendor
    template_name = "marketplace/vendor_list.html"
    queryset = Vendor.objects.filter(is_approved=True)


# class VendorDetailView(DetailView):
#     model = Vendor
#     template_name = "marketplace/vendor_detail.html"
    
#     slug_url_kwarg = "vendor_slug"
    

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context["categories"] = Category.objects.filter(vendor__slug=self.object.slug).prefetch_related(
#             Prefetch("food_cat", queryset=Food.objects.filter(is_available=True))
#         )
        
#         return context


class VendorDetailView(View):
    template_name = "marketplace/vendor_detail.html"

    
    def get(self, request, vendor_slug, cat_id=None):
        vendor = get_object_or_404(Vendor, slug=vendor_slug)
        working_hour = WorkingHours.objects.filter(vendor=vendor)
        
        category_side = Category.objects.filter(vendor__slug=vendor.slug)
        categories = Category.objects.filter(vendor__slug=vendor.slug).prefetch_related(
            Prefetch("food_cat", queryset=Food.objects.filter(is_available=True))
        )
        
        current_day = datetime.today().isoweekday()

        today_hour = working_hour.filter(days=current_day)
        

            # return False
        
        
        context ={
            'vendor': vendor,
            'category_side':category_side,
            'categories': categories,
            'working_hour': working_hour,
            'today_hour': today_hour
        }
        
        if cat_id:
                    
            categories = Category.objects.filter(pk=cat_id).prefetch_related('food_cat')
            context['categories']= categories
        print(context['categories'])
        return render(request, self.template_name, context)
    
    
    def post(self, request, *args, **kwargs):
        view = AddToCartView.as_view()
        return view(request, *args, **kwargs)


    

class AddToCartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)

        food_id = request.GET.get('food_id')
        quantity = int(request.GET.get('quantity'))

        
        food = get_object_or_404(Food, pk=food_id)
        
       
        cart.add(food, quantity)
   
        
        
        quantity = cart.cart[f'{food.vendor}-{food.slug}-{food.id}']['quantity']
        
        data = {
            'success': True,  # یا False اگر عملیات با مشکل مواجه شد
            'message': 'Food added to cart successfully',
            'cart_counter': cart.total(),
            'qty': quantity,
            'food_price':food.price * quantity,
            'cart_amount': cart.total_price()
            
        }
        
        return JsonResponse(data)


class DecreaseCartItem(View):
    def get(self, request):
        cart = Cart(request)
        food_id = request.GET.get('food_id')
        
        food = get_object_or_404(Food, id=food_id)
        
        cart.decrease(food)
        quantity = cart.cart[f'{food.vendor}-{food.slug}-{food.id}']['quantity']
        
        if quantity == 0:
            cart.remove(f'{food.vendor}-{food.slug}-{food.id}')
        
        data = {
                'success': True,
                'message': 'Food Decreased from cart successfully',
                'cart_counter': cart.total(),
                'qty': quantity,
                'food_price':food.price * quantity,
                
                'cart_amount': cart.total_price()
                
            }
        return JsonResponse(data)
    
    
    
class CartView(View):
    template_name = 'marketplace/cart_detail.html'
    
    def get(self, request):
        # context = {
        #       'grand_total': get_cart_total_price(request)
        #   }
        return render(request, self.template_name )
    
    
    # def post(self, request):
    #     flag = request.POST.get('flag')
    #     if flag:
    #         view = AddToCartView.as_view()
    #         return view(request)
        
        # view = CartDeleteView.as_view()
        # return view(request)

    
    
    
class CartDeleteView(View):
    
    def post(self, request):
        try:
            cart = Cart(request)
            item_id = request.POST.get('item_id')
            if item_id in cart:
                cart.remove(item_id)
                
                data = {
                    'status': 'Success',
                    'success': True,
                    'message': 'item successfully remove form cart',
                    'cart_counter': cart.total(),
                    
                }
        except:
            data = {
                'status': 'Failed',
                'message': 'Food quantity must be greater than 0',
            }
        return JsonResponse(data)
    
    
    
class Search(View):
    template_name = 'pages/search.html'
    def get(self, request):
        pass
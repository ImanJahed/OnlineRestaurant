from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from itertools import chain

from menu.models import Food
from vendors.models import Vendor

# Create your views here.
class HomePageView(View):
    template_name = 'pages/home.html'
    
    
    def get(self, request):
        vendors = Vendor.objects.filter(is_approved=True)
        papular_vendor = vendors[:3]
        context = {
            'vendors': vendors,
            'papular_vendor': papular_vendor
        }
        
        return render(request, self.template_name, context)
    
    
    
    
class SearchView(View):
    template_name ='pages/search.html'

    def get(self,request):
        q = request.GET.get('q')
        vendors = Vendor.objects.filter(name__icontains=q)
        foods = Food.objects.filter(Q(food_name__icontains=q) | Q(vendor__name__icontains=q))
        
        results = chain(vendors, foods)

        context = {
            'results': results,
            'q': q
        }
        return render(request, self.template_name, context)
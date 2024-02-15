from django.shortcuts import get_object_or_404
from menu.models import Category, Food
from vendors.models import Vendor
from .cart import Cart


def cart(request):
    cart = Cart(request)
    
    vendor_ids = list(set(item['vendor_id'] for item in cart))
    total_shipment = sum([vendor.shipment for vendor in Vendor.objects.filter(id__in=vendor_ids)])
      
    return dict(cart=cart, total_shipment=total_shipment)




       
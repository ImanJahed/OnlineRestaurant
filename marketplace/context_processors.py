from django.shortcuts import get_object_or_404
from menu.models import Category, Food
from .cart import Cart


def cart(request):
    return dict(cart=Cart(request))




       
import json
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from menu.models import Food
from django.core import serializers

SESSION_CART_KEY = "cart"


class Cart:
    def __init__(self, request):
        """
        Initialize Cart
        """

        self.session = request.session

        # if cart exists in session equal to cart
        cart = self.session.get(SESSION_CART_KEY)

        # if cart not exists in session create one
        if not cart:
            cart = self.session[SESSION_CART_KEY] = {}

        # for cart available in whole of class
        self.cart = cart

    def _generate_unique_food_id(self, food):
        """
        generate the unique id for food

        Args:
            vendor (str): The name of the vendor who provided the food
            food_slug (str): food's slug

        Returns:
            str: unique id for food
        """
        return f"{food.vendor}-{food.slug}-{food.id}"

    def add(self, food, quantity=1):
        """
        Add Item to Cart

        Args:
            food (int): food's id ordered
            quantity (int): quantity of food ordered. Defaults to 1.
        """

        food_id = self._generate_unique_food_id(food)

        if food_id not in self.cart:
            self.cart[food_id] = {
                "food_name": food.food_name,
                "quantity": 1,
                "vendor_id": food.vendor.name,
                "id": food.id,
                'food_id': food_id
            }
        else:
            self.cart[food_id]["quantity"] += 1

        self.save()
        
    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            # برای تبدیل یه کوئری ست به جیسون به دو روش میتوان عمل کرد
            
            # 1- 
            # from django.core.serializers import serialize
            # food_json = serialize("json", Food.objects.all())
            # 2-
            # food_list = list(Food.objects.values())

            
            
            food = get_object_or_404(Food, pk=item['id'])  # برای تبدیل کرد آبحکت یک مدل به جیسون  (json) 
            # item['food'] = model_to_dict(food)
            # item['food'] = serializers.serialize('json', [food], fields=['vendor', 'category', 'food_name', 'description', 'slug', 'price', 'duration', 'is_available', 'food_img'])
            # item['food']['food_img'] = food.food_img.url if food.food_img else ''
           
            item['price'] = food.price
            item['total_item_price'] = item['quantity'] * item['price']
            item['food_id'] = self._generate_unique_food_id(food)
            yield item
        
    def decrease(self, food):
        food_id = self._generate_unique_food_id(food)
        
        if self.cart[food_id]['quantity'] >= 1:
            self.cart[food_id]['quantity'] -= 1
       
            
        self.save()
        
        
    def total(self):
        """
        All quantity item in the cart
        """
        
        return sum(item["quantity"] for item in self.cart.values())

    def total_price(self):
        
        return sum(item['total_item_price'] for item in self)
    
        # total = 0
        # for item in self:
        #     total += item['total_item_price']
        # return total


    def remove(self, food_id):
        """
        Remove food from cart with food id

        Args:
            food_id (str): get food id which must be remove from cart
        """

        if food_id in self.cart.keys():
            del self.cart[food_id]
            self.save()

    def clear(self):
        """
        Clear whole of cart
        """
        self.cart.clear()
        self.save()

    def save(self):
        """
        Save All Change in Session
        """
        self.session.modified = True

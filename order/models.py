import json
import random
import string
from django.db import models
from django.contrib.auth import get_user_model
from marketplace.cart import Cart
from menu.models import Food

from vendors.models import Vendor

User = get_user_model()

request_object = ''
# Create your models here.
class Order(models.Model):
    
    STATUS_CHOICES = (
        (1,'Confirm'),
        (2,'Preparing'),
        (3,'Sending'),
        (4,"Delivered"),
        (5,"Canceled"),
    )
    
    
    order_id = models.CharField(max_length=13)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    vendors = models.ManyToManyField(Vendor, blank=True)
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=12)
    email = models.EmailField(blank=True, null=True)
    
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    
    total_price = models.FloatField()
    total_shipment = models.FloatField(default=0)
    
    vendor_share = models.JSONField(blank=True, null=True)
    admin_share = models.FloatField(blank=True, null=True)

    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    is_paid = models.BooleanField(default=False)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.order_id}-{self.user.phone_number}'
            
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def _generate_order_id(self):
        rand = random.SystemRandom()
        digit_rand = rand.choices(string.digits, k=6)

        return ''.join(digit_rand)
    
    
    def order_placed_to(self):
        return ', '.join([str(i) for i in self.vendors.all()])
    
            
                
    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)        
        
        if self.vendor_share:
            vendor_data = json.loads(self.vendor_share)
            total = vendor_data.get(str(vendor.id))
            admin_share = (total * (100/90)) * (10/100)
            total += vendor.shipment
            
            return dict(total=total, admin_share=admin_share)

    def admin_share(self):
        return self.total_price * (10/100) 
    
    def save(self, *args, **kwargs):
        try:
            if self.pk is not None:
                return super().save(*args, **kwargs)
            
            else:
                self.status = self.STATUS_CHOICES[0][0]
                self.order_id = f'order-{self._generate_order_id()}'
                cart = Cart(request_object)
                vendor_share = {}
                
                for item in cart.cart.values():
                    
                    if item['vendor_id'] not in vendor_share:
                        vendor_share[item['vendor_id']] = item['total_item_price'] * (90/100)
                    else:
                        vendor_share[item['vendor_id']] += item['total_item_price'] * (90/100)
                
                self.vendor_share = json.dumps(vendor_share)
                self.admin_share = cart.total_price() * (10/100) 
            
        
        except:
            pass

        
        return super().save(*args, **kwargs)
    
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food,  on_delete=models.CASCADE, related_name='food_item')
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f'{self.order.order_id}-{self.food.food_name}'
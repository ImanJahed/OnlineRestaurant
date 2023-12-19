import random
import re
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime


from .manager import CustomManager





# Create your models here.
def check_phone(phone):
    valid_phone = '09(0[0-9]|1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}'
    if not re.match(valid_phone, phone):
        raise ValidationError('Phone not Valid')
    return phone


class User(AbstractBaseUser):
    ROLL_CHOICE = (
        (1, 'Customer'),
        (2, 'Vendor')
    )

    
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('Phone Number'), validators=[check_phone])
    email = models.EmailField(verbose_name=_('Email'), unique=True, null=True, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    roll = models.SmallIntegerField(choices=ROLL_CHOICE, null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = 'phone_number'

    objects = CustomManager()
    
    def __str__(self):
        return self.phone_number
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    
    
    
def image_path_profile(instance, filename):
    return f'img/{instance.user.phone_number}/{instance.filed_name}/{filename}'
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    province = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    img_cover = models.ImageField(upload_to=image_path_profile, null=True, blank=True)
    img_profile = models.ImageField(upload_to=image_path_profile, null=True, blank=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    
    def __str__(self):
        return self.user.phone_number

    @property
    def get_full_name(self):
        return f'{self.fist_name} {self.last_name}'
    
    
    
    
class OTPCode(models.Model):
    phone_number = models.CharField(_("Phone Number"), max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    expired_at = models.DateTimeField(default= timezone.now() + datetime.timedelta(seconds=120))
    
    
    def __str__(self):
        return self.phone_number
    
    def generate_code(self):
        self.code = self._rand_code()
        self.expired_at = timezone.now() + datetime.timedelta(seconds=120)
    
    def _rand_code(self):
        rand = random.SystemRandom()
        digit = rand.choices(string.digits, k=6)
        
        return ''.join(digit)
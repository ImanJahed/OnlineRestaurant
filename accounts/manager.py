from django.contrib.auth.models import BaseUserManager, UserManager

from django.utils.translation import gettext_lazy as _

class CustomManager(BaseUserManager):
    def create_user(self, phone_number, password=None, email=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone Number must be set!')
        
        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            **extra_fields,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    def create_superuser(self, phone_number,password=None, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(phone_number, email=email, password=password, **extra_fields)

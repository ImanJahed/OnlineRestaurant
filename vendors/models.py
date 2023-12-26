from collections.abc import Iterable
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import Profile, User

def vendor_path_file(instance, filename):
    return f'restaurant_img/{instance.name}/{instance.user}/{filename}'
    
def vendor_path_image(instance, filename):
    return f'restaurant_img/{instance.name}/{instance.user}/{filename}'
    
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_user')
    vendor_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='vendor_profile')
    name = models.CharField(max_length=50)

    license_file = models.FileField(upload_to=vendor_path_file)
    profile_img = models.ImageField(upload_to=vendor_path_image, blank=True, null=True)
    cover_img = models.ImageField(upload_to=vendor_path_image, blank=True, null=True)
    
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                # send email to vendor
                mail_template = 'accounts/email/email_approved.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email
                }
                message = render_to_string(mail_template, context)
                
                if self.is_approved:
                    mail_subject = 'Congratulations, Your restaurant has been approved.'
                    send_mail(mail_subject, message, 'admin@gmail.com', [self.user.email], fail_silently=True)
                else:
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_mail(mail_subject, message, 'admin@gmail.com', [self.user.email], fail_silently=True)


        return super().save(*args, **kwargs)
from django.db import models

from accounts.models import Profile, User

def vendor_path_file(instance, filename):
    return f'{instance.name}/{instance.user}/{filename}'
    
def vendor_path_image(instance, filename):
    return f'{instance.name}/{instance.user}/{filename}'
    
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
    
    
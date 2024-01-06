
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import Profile, User
from datetime import time, datetime


def vendor_path_file(instance, filename):
    return f'restaurant_img/{instance.name}/{instance.user}/{filename}'
    
    
# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_user')
    vendor_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='vendor_profile')
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    license_file = models.FileField(upload_to=vendor_path_file)
    
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def is_open(self):
        current_day = datetime.now().isoweekday()
        current_time = datetime.now().strftime('%H:%M %p')

        opening_day_time = WorkingHours.objects.filter(vendor=self, days=current_day)
        
        
        for i in opening_day_time:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, "%H:%M %p").time())
                end = str(datetime.strptime(i.to_hour, "%H:%M %p").time())
                
                if start < current_time < end:
                    return True
                
            return False
            
        
        
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
    
    
class WorkingHours(models.Model):
    DAYS = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    
    HOURS_OF_DAY_24 = [(time(h,m).strftime('%H:%M %p'), time(h,m).strftime('%H:%M %p')) for h in range(0,24) for m in (0,30)]
    
    vendor = models.ForeignKey(Vendor,  on_delete=models.CASCADE)
    days = models.SmallIntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOURS_OF_DAY_24, blank=True, null=True, max_length=30)
    to_hour = models.CharField(choices=HOURS_OF_DAY_24, blank=True, null=True, max_length=30)

    is_closed = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('days',)
        unique_together = ('vendor', 'days', 'from_hour', 'to_hour')
        
        
    def __str__(self):
        return self.get_days_display()
    
    
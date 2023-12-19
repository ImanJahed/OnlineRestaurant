from django.urls import path

from . import views


urlpatterns = [
    # user register and sign up
    path('send-otp/', views.SendOtp.as_view(), name='send_otp'),
    path('check-otp/', views.OTPCodeCheck.as_view(), name='check_otp'),
    
    # vendor register
    path('vendor-register/', views.VendorRegister.as_view(), name='vendor_register'),

    
    # logout
    path('logout/', views.LogOutUserView.as_view(), name='logout'),

    
]

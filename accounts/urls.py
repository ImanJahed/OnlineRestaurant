from django.urls import path
from django.contrib.auth import views as auth_view
from . import views


urlpatterns = [
    # user register and sign up
    path('send-otp/', views.SendOtp.as_view(), name='send_otp'),
    path('check-otp/', views.OTPCodeCheck.as_view(), name='check_otp'),
    
    # vendor register
    path('vendor-register/', views.VendorRegister.as_view(), name='vendor_register'),

    # logout
    path('logout/', views.LogOutUserView.as_view(), name='logout'),
    
    # profiles
    path('profile/', views.ProfileDispatcher.as_view(), name='profile_dispatcher'),
    # ---------------------Customer Dashboard----------------------------------------
    
    # customer profile
    path('CustomerDashboard/', views.CustomerProfileView.as_view(), name='customer_profile'),
    
    
    # Customer Edit Profile
    path('ProfileSettings/', views.CustomerEditProfileView.as_view(), name='edit_profile'),
    
    # Change Password
    path('ChangePassword/', auth_view.PasswordChangeView.as_view(), name='change_password'),

    # Change password Done
    path('ChangePasswordDone/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Set Password
    path('SetPassword/', views.CustomerSetPassword.as_view(), name='set_password'),
    
    # ----------------------Admin Dashboard-------------------------------------------

    # admin profile
    path('AdminDashboard/', views.AdminDashboardView.as_view(), name='admin_profile'),
    # Admin Order Detail
    path("OrderDetail/<int:pk>/", views.AdminOrderDetailView.as_view(), name="admin_order_detail"),
    
    # Admin Earnings 
    path("AdminEarnings/", views.AdminEarningsView.as_view(), name="admin_earning")
    
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.CheckOutView.as_view(), name='checkout'),
    path('OrderComplete/', views.OrderCompleteView.as_view(), name='order_complete'),
]

from django.urls import path

from . import views


urlpatterns = [
    path('', views.VendorListView.as_view(), name='vendor_list'),
    path('food/<slug:vendor_slug>/', views.VendorDetailView.as_view(), name='vendor_detail'),
    path('food/<slug:vendor_slug>/<int:cat_id>', views.VendorDetailView.as_view(), name='food_cat'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('decreaseCartItem/', views.DecreaseCartItem.as_view(), name='decrease_cart_item'),

    path('CartDetail/', views.CartView.as_view(), name='cart'),

    path('deleteItem/', views.CartDeleteView.as_view(), name='cart_delete'),

]

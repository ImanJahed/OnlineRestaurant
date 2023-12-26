from django.urls import path

from . import views
from menu import views as menu_views


app_name = 'vendors'

urlpatterns = [
    # Dashboard
    path('VendorDashboard', views.VendorProfile.as_view(), name='vendor_dashboard'),
    path('EditRestaurant', views.VendorEditProfileView.as_view(), name='vendor_edit'),
    
    # MenuBuilder
    path('MenuBuilder/', menu_views.MenuBuilderView.as_view(), name='menu_builder'),
    # Category Crud
    path('MenuBuilder/category/', menu_views.CategoryListView.as_view(), name='category_list'),
    path('MenuBuilder/category/add/', menu_views.CategoryCreateView.as_view(), name='category_create'),
    path('MenuBuilder/category/<slug:slug>/', menu_views.CategoryDetailView.as_view(), name='category_detail'),
    path('MenuBuilder/category/edit/<int:pk>/', menu_views.CategoryUpdateView.as_view(), name='category_update'),
    path('MenuBuilder/category/delete/<int:pk>/', menu_views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Food Crud
    path('MenuBuilder/food/add', menu_views.FoodCreateView.as_view(), name='food_create'),
    path('MenuBuilder/food/edit/<int:pk>/', menu_views.FoodUpdateView.as_view(), name='food_update'),
    path('MenuBuilder/food/delete/<int:pk>/', menu_views.FoodDeleteView.as_view(), name='food_delete'),
]

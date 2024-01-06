from django.db.models.base import Model as Model

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from menu.forms import CategoryForm, FoodForm

from menu.models import Category, Food

# Create your views here.


# Send Request To Form Model
class PassRequestToFormMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class MenuBuilderView(ListView):
    model = Food
    template_name = "menu/menu_builder.html"
    context_object_name = "foods"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(vendor__user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.filter(vendor__user=self.request.user)
        return context


# ------------------------------------------------
# Category Crud


class CategoryCreateView(PassRequestToFormMixin, CreateView):
    template_name = "menu/add_category.html"
    form_class = CategoryForm

    success_url = reverse_lazy("vendors:menu_builder")


class CategoryListView(ListView):
    model = Category
    template_name = "menu/category_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(vendor__user=self.request.user)
        return qs


class CategoryUpdateView(PassRequestToFormMixin, UpdateView):
    model = Category
    template_name = "menu/category_update.html"
    form_class = CategoryForm
    success_url = reverse_lazy("vendors:menu_builder")

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(vendor__user=self.request.user)
        return qs


class CategoryDetailView(DetailView):
    model = Category
    template_name = "menu/food_list.html"
    ordering = "created_at"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        foods = category.food_cat.all().order_by("-created_at")
        context["foods"] = foods
        return context


# class CategoryDeleteView(View):
#     def get(self,request,pk):
#         return self.post(request, pk)
#     def post(self, request, pk):
#         obj = get_object_or_404(Category, pk=pk)
#         obj.delete()
#         return redirect('vendors:menu_builder')


class CategoryDeleteView(DeleteView):
    model = Category

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("vendors:menu_builder")


# --------------------------------------------------------
# Food Curd


class FoodCreateView(PassRequestToFormMixin, CreateView):
    # model = Food
    template_name = "menu/food_add.html"
    form_class = FoodForm

    success_url = reverse_lazy("vendors:menu_builder")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.filter(vendor__user=self.request.user)
        return context


class FoodUpdateView(PassRequestToFormMixin, UpdateView):
    model = Food
    form_class = FoodForm
    template_name = "menu/food_update.html"

    def get_success_url(self) -> str:
        updated_food = self.get_object()
        category = updated_food.category

        return reverse("vendors:category_detail", kwargs={"slug": category.slug})

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     qs = qs.filter(vendor__user=self.request.user)
    #     return qs


class FoodDeleteView(DeleteView):
    model = Food

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("vendors:menu_builder")

from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Product, Category

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class AddProductView(CreateView):
    model = Product
    template_name = 'catalog/add_product.html'
    fields = ['name', 'description', 'image', 'category', 'price']
    success_url = reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
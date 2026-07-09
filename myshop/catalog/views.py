from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product

def home(request):
    products_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'catalog/home.html', {'products': products})

def catalog(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'catalog/catalog.html', {'products': products})

def contacts(request):
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})



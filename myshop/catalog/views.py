from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Product, Category


def home(request):
    # Получаем все товары
    products_list = Product.objects.all()

    # Пагинация (доп. задание)
    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'catalog/home.html', {'products': products})


def product_detail(request, pk):
    # Получаем товар по pk
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog/catalog.html', {'products': products})


def contacts(request):
    return render(request, 'catalog/contacts.html')


# Доп. задание: Добавление товара
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')

        if name and description and price and category_id:
            category = Category.objects.get(id=category_id)
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category
            )
            return redirect('catalog:home')

    categories = Category.objects.all()
    return render(request, 'catalog/add_product.html', {'categories': categories})

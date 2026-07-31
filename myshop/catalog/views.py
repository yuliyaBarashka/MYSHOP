from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .models import Product, Category
from .forms import ProductForm
from .services import ProductService


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('-created_at')


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем категории в контекст
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        # Используем сервис для получения продукта с кешированием
        product = ProductService.get_product_detail(self.kwargs.get('pk'))
        if product is None:
            raise PermissionDenied("Продукт не найден")
        return product


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        context['button_text'] = 'Добавить товар'
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
            return obj
        raise PermissionDenied("У вас нет прав на редактирование этого продукта")

    def form_valid(self, form):
        # Очищаем кеш при обновлении
        ProductService.clear_product_cache(self.object.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование товара'
        context['button_text'] = 'Сохранить изменения'
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
            # Очищаем кеш при удалении
            ProductService.clear_product_cache(obj.id)
            return obj
        raise PermissionDenied("У вас нет прав на удаление этого продукта")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление товара'
        return context


class ProductModerateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    fields = ['is_published']
    template_name = 'catalog/product_moderate.html'
    permission_required = 'catalog.can_unpublish_product'

    def get_success_url(self):
        # Очищаем кеш после модерации
        ProductService.clear_product_cache(self.object.id)
        return reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Модерация товара'
        return context


# Новое представление для отображения продуктов по категории
class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        # Используем сервис для получения продуктов с кешированием
        return ProductService.get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            context['category'] = category
        except Category.DoesNotExist:
            context['category'] = None
        return context
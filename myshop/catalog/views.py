from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .forms import ProductForm
from .services import ProductService

# ============================================
# PUBLIC VIEWS - доступны всем пользователям
# ============================================

class HomeView(ListView):
    """Главная страница - доступна всем"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('-created_at')


class CatalogView(ListView):
    """Каталог продуктов - доступен всем"""
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    """Детальная страница продукта - доступна всем"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        return ProductService.get_product_detail(self.kwargs.get('pk'))


class ContactsView(TemplateView):
    """Страница контактов - доступна всем"""
    template_name = 'catalog/contacts.html'


class CategoryProductsView(ListView):
    """Список продуктов в категории - доступен всем"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
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


# ============================================
# PROTECTED VIEWS - ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ
# ============================================

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта - только для авторизованных пользователей"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        # Automatically set owner to current user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        context['button_text'] = 'Добавить товар'
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта - только для авторизованных владельцев или модераторов"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        # Check: owner OR moderator can edit
        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
            return obj
        raise PermissionDenied("У вас нет прав на редактирование этого продукта")

    def form_valid(self, form):
        # Clear cache after update
        ProductService.clear_product_cache(self.object.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование товара'
        context['button_text'] = 'Сохранить изменения'
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта - только для авторизованных владельцев или модераторов"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:catalog')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        # Check: owner OR moderator can delete
        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
            # Clear cache before deletion
            ProductService.clear_product_cache(obj.id)
            return obj
        raise PermissionDenied("У вас нет прав на удаление этого продукта")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление товара'
        return context


class ProductModerateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Модерация продукта - только для пользователей с правом can_unpublish_product"""
    model = Product
    fields = ['is_published']
    template_name = 'catalog/product_moderate.html'
    permission_required = 'catalog.can_unpublish_product'

    def get_success_url(self):
        # Clear cache after moderation
        ProductService.clear_product_cache(self.object.id)
        return reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Модерация товара'
        return context
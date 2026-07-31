from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .forms import ProductForm


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        # Показываем только опубликованные продукты
        return Product.objects.filter(is_published=True).order_by('-created_at')


class CatalogView(ListView):
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Показываем только опубликованные продукты
        return Product.objects.filter(is_published=True).order_by('-created_at')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        # Автоматически привязываем владельца
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

        # Проверяем права: владелец или модератор может редактировать
        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
            return obj
        raise PermissionDenied("У вас нет прав на редактирование этого продукта")

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

        # Проверяем права: владелец или модератор может удалить
        if obj.owner == user or user.has_perm('catalog.can_unpublish_product'):
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
        return reverse_lazy('catalog:catalog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Модерация товара'
        return context
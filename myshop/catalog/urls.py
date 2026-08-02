from django.urls import path
from .views import (
    HomeView, CatalogView, ProductDetailView,
    ContactsView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, ProductModerateView, CategoryProductsView
)

app_name = 'catalog'

urlpatterns = [
    # ============================================
    # PUBLIC URLS - доступны всем пользователям
    # ============================================
    path('', HomeView.as_view(), name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),

    # ============================================
    # PROTECTED URLS - только для авторизованных
    # ============================================
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/moderate/', ProductModerateView.as_view(), name='product_moderate'),
]
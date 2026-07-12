from django.urls import path
from .views import (
    HomeView, CatalogView, ProductDetailView,
    ContactsView, AddProductView
)

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('add/', AddProductView.as_view(), name='add_product'),
]
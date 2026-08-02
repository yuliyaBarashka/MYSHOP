from django.core.cache import cache
from .models import Product, Category


class ProductService:
    """Сервис для работы с продуктами с кешированием"""

    @staticmethod
    def get_products_by_category(category_id):
        """Получить все продукты в категории с кешированием"""
        cache_key = f'category_{category_id}'
        products = cache.get(cache_key)

        if products is None:
            # Если данных нет в кеше, получаем из БД
            try:
                category = Category.objects.get(id=category_id)
                products = category.products.filter(is_published=True)
                # Сохраняем в кеш на 5 минут (300 секунд)
                cache.set(cache_key, products, timeout=300)
            except Category.DoesNotExist:
                products = []

        return products

    @staticmethod
    def get_product_detail(product_id):
        """Получить детальную информацию о продукте с кешированием"""
        cache_key = f'product_{product_id}'
        product = cache.get(cache_key)

        if product is None:
            try:
                product = Product.objects.get(id=product_id, is_published=True)
                cache.set(cache_key, product, timeout=300)
            except Product.DoesNotExist:
                product = None

        return product

    @staticmethod
    def clear_product_cache(product_id):
        """Очистить кеш продукта"""
        cache.delete(f'product_{product_id}')
        # Также очищаем кеш категории
        try:
            product = Product.objects.get(id=product_id)
            cache.delete(f'category_{product.category.id}')
        except Product.DoesNotExist:
            pass

    @staticmethod
    def get_all_categories():
        """Получить все категории с кешированием"""
        cache_key = 'all_categories'
        categories = cache.get(cache_key)

        if categories is None:
            categories = Category.objects.all()
            cache.set(cache_key, categories, timeout=3600)  # 1 час

        return categories
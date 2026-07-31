from django.core.management.base import BaseCommand
from catalog.models import Product


class Command(BaseCommand):
    help = 'Fill database with test products'

    def handle(self, *args, **options):
        products_data = [
            {
                'name': 'Смартфон Galaxy S25',
                'description': 'Флагманский смартфон с большим экраном и отличной камерой. Поддерживает 5G, имеет защиту от воды.',
                'price': 999.99
            },
            {
                'name': 'Ноутбук ProBook 15',
                'description': 'Мощный ноутбук для работы и учебы. Процессор Intel Core i7, 16GB RAM, SSD 512GB.',
                'price': 1499.99
            },
            {
                'name': 'Наушники AirPods Pro',
                'description': 'Беспроводные наушники с активным шумоподавлением и отличным звуком.',
                'price': 249.99
            },
            {
                'name': 'Умные часы Watch Series 9',
                'description': 'Смарт-часы с отслеживанием здоровья, GPS и большим дисплеем.',
                'price': 399.99
            },
            {
                'name': 'Планшет Tab S9',
                'description': 'Планшет с большим экраном, подходит для работы и развлечений.',
                'price': 649.99
            },
            {
                'name': 'Игровая приставка Pro',
                'description': 'Игровая консоль нового поколения с поддержкой 4K и быстрой загрузкой игр.',
                'price': 499.99
            }
        ]

        for product_data in products_data:
            Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS(f'Добавлено {len(products_data)} товаров!'))

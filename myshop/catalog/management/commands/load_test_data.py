from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product, Contact


class Command(BaseCommand):
    help = 'Загружает тестовые данные из фикстур'

    def handle(self, *args, **options):
        self.stdout.write('🗑️ Удаление существующих данных...')

        # Удаляем все данные
        Product.objects.all().delete()
        Category.objects.all().delete()
        Contact.objects.all().delete()

        self.stdout.write('📥 Загрузка данных из фикстур...')

        try:
            call_command('loaddata', 'catalog/fixtures/categories.json')
            self.stdout.write(self.style.SUCCESS('✅ Категории загружены'))

            call_command('loaddata', 'catalog/fixtures/products.json')
            self.stdout.write(self.style.SUCCESS('✅ Продукты загружены'))

            call_command('loaddata', 'catalog/fixtures/contacts.json')
            self.stdout.write(self.style.SUCCESS('✅ Контакты загружены'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: {e}'))
            return

        self.stdout.write(self.style.SUCCESS(
            f'\n📊 Статистика:\n'
            f'  Категории: {Category.objects.count()}\n'
            f'  Продукты: {Product.objects.count()}\n'
            f'  Контакты: {Contact.objects.count()}'
        ))

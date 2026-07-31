from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает права'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Создание группы "Модератор продуктов"...')

        # Получаем ContentType для Product
        content_type = ContentType.objects.get_for_model(Product)

        # Создаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write('ℹ️ Группа "Модератор продуктов" уже существует')

        # Получаем права
        permissions = [
            'can_unpublish_product',  # Может отменять публикацию
            'delete_product',  # Может удалять продукты
        ]

        # Назначаем права группе
        for codename in permissions:
            try:
                permission = Permission.objects.get(
                    content_type=content_type,
                    codename=codename
                )
                moderator_group.permissions.add(permission)
                self.stdout.write(f'  ✅ Добавлено право: {codename}')
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠️ Право "{codename}" не найдено'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Группа "Модератор продуктов" создана успешно!'))
        self.stdout.write('\n📝 Инструкция:')
        self.stdout.write('  1. Зайдите в админку: http://127.0.0.1:8000/admin/')
        self.stdout.write('  2. Найдите пользователя, которому хотите дать права модератора')
        self.stdout.write('  3. Добавьте его в группу "Модератор продуктов"')
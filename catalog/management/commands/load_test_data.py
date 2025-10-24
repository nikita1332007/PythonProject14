from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Load test data for products and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write('Очистка существующих данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Добавление новых категорий...')
        cat1 = Category.objects.create(name='Техника', description='Электронные устройства')
        cat2 = Category.objects.create(name='Одежда', description='Модные вещи')

        self.stdout.write('Добавление продуктов...')
        products = [
            {'name': 'Ноутбук', 'description': 'Мощный и лёгкий', 'category': cat1, 'price': 55000},
            {'name': 'Куртка', 'description': 'Тёплая зимняя', 'category': cat2, 'price': 12000},
        ]

        for prod in products:
            Product.objects.create(**prod)

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены'))
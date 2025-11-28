from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        content_type = ContentType.objects.get_for_model(Product)
        can_unpublish = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        can_delete = Permission.objects.get(codename='delete_product', content_type=content_type)

        group.permissions.add(can_unpublish, can_delete)
        group.save()
        self.stdout.write("Группа 'Модератор продуктов' создана и права назначены.")
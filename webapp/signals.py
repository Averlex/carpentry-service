from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User, Order


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name == 'webapp':  # Ensure this only runs for your app
        content_types = ContentType.objects.get_for_model(Order)
        permission, _ = Permission.objects.get_or_create(
            codename='webapp.all_orders_access',
            name='Has an access to all orders (including order editor',
            content_type=content_types
        )
        groups_permissions = {
            'Администратор': {
                'permissions': Permission.objects.all(),
                'is_superuser': True,
                'is_staff': True,
                'match': 0,
            },
            'Сотрудник мастерской': {
                'permissions': [
                    # Only one needed to watch and manage orders
                    permission,
                ],
                'is_superuser': False,
                'is_staff': False,
                'match': 1,
            },
            'Довольный клиент': {
                'permissions': [
                    # Not needed here
                ],
                'is_superuser': False,
                'is_staff': False,
                'match': 2,
            },
        }

        for group_name, config in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(config['permissions'])

            users = User.objects.filter(user_group=groups_permissions[group_name]['match'])

            for user in users:
                user.is_superuser = config['is_superuser']
                user.is_staff = config['is_staff']
                user.groups.add(group)
                user.save()

                group = Group.objects.get(name=group_name)
                group.user_set.add(user)
                group.save()

                print(f'Successfully assigned permissions to {user.username}')

        try:
            superuser = User.objects.get(username='super')

        except User.DoesNotExist as err:
            superuser = User.objects.create_superuser(
                username="super", password="test", email="super@test.com", phone='00000000000'
            )
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_active = True
        superuser.is_superuser = True
        admin_group = Group.objects.get(name='Администратор')
        superuser.groups.add(admin_group)
        superuser.groups.remove(Group.objects.get(name='Довольный клиент'))
        admin_group.user_set.add(superuser)
        Group.objects.get(name='Довольный клиент').user_set.remove(superuser)
        superuser.user_permissions.add(permission)
        superuser.save()

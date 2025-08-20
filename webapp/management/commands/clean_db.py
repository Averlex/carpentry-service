from django.core.management.base import BaseCommand
from webapp.models import FAQ, UserFeedback, Order, Product, ProductList, Delivery, User


class Command(BaseCommand):
    help = 'Clean the database by deleting all records from tables'

    def handle(self, *args, **kwargs):
        deliveries_deleted, _ = Delivery.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deliveries_deleted} deliveries'))

        orders_deleted, _ = Order.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {orders_deleted} orders'))

        product_lists_deleted, _ = ProductList.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {product_lists_deleted} product lists'))

        products_deleted, _ = Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {products_deleted} products'))

        user_feedbacks_deleted, _ = UserFeedback.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {user_feedbacks_deleted} user feedbacks'))

        users_deleted, _ = User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {users_deleted} users'))

        faqs_deleted, _ = FAQ.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {faqs_deleted} FAQs'))

from django.contrib import admin
from .models import FAQ, UserFeedback, User, Order, Product, ProductList, Delivery

admin.site.register(FAQ)
admin.site.register(UserFeedback)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(ProductList)
admin.site.register(Delivery)

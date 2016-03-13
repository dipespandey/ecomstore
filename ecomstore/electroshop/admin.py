from django.contrib import admin
from .models import Product
from .models import Category
from .models import UserProfile
from .models import CartItem


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(CartItem)

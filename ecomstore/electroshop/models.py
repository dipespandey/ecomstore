from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
    	return self.category


class Product(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(max_length=150)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    product_id = models.IntegerField(unique=True)
    desc = models.TextField()
    price = models.DecimalField(max_digits=9,decimal_places=2)
    old_price=models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00)
    image = models.ImageField(upload_to='static/images')
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField()
    
    # def sale_price(self):
    #     if self.old_price > self.price:
    #         return self.price
    #     else:
    #         return None

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    picture = models.ImageField(upload_to='profile_images',blank=True)
    phone = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username



class CartItem(models.Model):
    cart = models.ForeignKey('Cart', null=True, blank=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default = timezone.now)
    quantity = models.IntegerField(default = 1)
    product = models.ForeignKey('Product')

    # def __str__(self):
    #     return self.date_added

    def total(self):
        return self.quantity*self.product.price


    def price(self):
        return self.product.price

    def augment_quantity(self,quantity):
        self.quantity = self.quantity+int(quantity)
        self.save()
    


class Cart(models.Model):
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Cart id: %s" %(self.id)

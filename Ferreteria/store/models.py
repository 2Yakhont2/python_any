from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.utils import timezone

from ecommerce.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
     
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', default='products/default.png', blank=True, null=True)
    slug = models.SlugField(max_length=255)
    stock = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Reactivar el producto si su stock es mayor que 0
        if self.stock > 0:
            self.is_active = True
        else:
            self.is_active = False  ### Si el stock es 0 o menor, desactivar el producto
            
        super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
    def get_total_price(self):
        return self.product.price * self.quantity
    

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total_price = sum(order.get_total_price() for order in self.orders.all())
        return total_price
    



from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price2 = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_new = models.BooleanField()
    is_discounted = models.BooleanField()
    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('shop.Brand', on_delete=models.CASCADE)
    thumb = models.ImageField(default='default.jpg')
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'shop_products'


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'shop_categories'


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = 'shop_brands'


class Slide(models.Model):
    image = models.ImageField(default='default.jpg')

    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'
        db_table = 'shop_slides'

class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    def total_price(self):
        return self.product.price * self.quantity



class Order(models.Model):
    STATUS_CHOICES = [
        ('В рассмотрении', 'В рассмотрении'),
        ('Заказ принят', 'Заказ принят'),
        ('Ваш заказ уже в пути', 'Ваш заказ уже в пути'),
        ('dЗаказ прибыл', 'Заказ прибыл'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Не оплачен', 'Не оплачен'),
        ('Оплачено', 'Оплачено'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)  # Изменил на CharField для хранения телефонных номеров в международном формате
    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f"Заказ #{self.pk}"


class OrderProduct(models.Model):
    order = models.ForeignKey('shop.Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    amount = models.IntegerField()
    total = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.product} x{self.amount} - {self.order.customer.username}"


RATE_CHOICES = [
   (1, '1 - Очень плохо'),
   (2, '2 - Плохо'),
   (3, '3 - не очень'),
   (4, '4 - Хорошо'),
   (5, '5 - Отлично!'),
]
class Review(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   date = models.DateTimeField(auto_now_add=True)
   text = models.TextField(blank=True)
   rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

   def __str__(self):
       return self.user.username



class other(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    price = models.IntegerField(null=True)
    number = models.CharField(max_length=100)
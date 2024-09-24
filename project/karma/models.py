from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
# Create your models here.
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

# ======================= CATEGORY ============================


class Category(models.Model):
    title = models.CharField('Sarlavha', db_index=True, max_length=255)
    slug = models.SlugField('manzil', unique=True)
    date = models.DateTimeField('Vaqt', default=timezone.now)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})


class Brend(models.Model):
    title = models.CharField('Sarlavha', db_index=True, max_length=255)
    slug = models.SlugField('manzil', unique=True)
    date = models.DateTimeField('Vaqt', default=timezone.now)

    class Meta:
        verbose_name = 'Brend'
        verbose_name_plural = 'Brendlar'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('brend_detail_url', kwargs={'slug': self.slug})


class Product(models.Model):
    title = models.CharField('Sarlavha', max_length=255, db_index=True)
    popular = models.IntegerField('ko`rilganlar soni', default=0)
    image_1 = models.ImageField('Rasm 1')
    image_2 = models.ImageField('Rasm 2')
    image_3 = models.ImageField('Rasm 3')
    text = models.TextField('Taxt')
    slug = models.SlugField('Manzil', unique=True)
    price = models.IntegerField('Narx', default=0)
    date = models.DateTimeField('Vaqt', default=timezone.now)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, related_name='category_set')
    brend = models.ForeignKey(
        Brend, related_name='brend_set', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title

    def discount(self):
        return self.price + (self.price // 10)

    
    def get_absolute_url(self):
        return reverse('product_detail_url', kwargs={'slug': self.slug})

# ========================= CART ==============================


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class OrderStatus(models.Model):
    name = models.CharField(max_length=255)
    system_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    name = models.CharField(max_length=255)
    system_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')
    total = models.IntegerField(default=0)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT)


class Orderproduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)
    product_price = models.IntegerField(default=0)
    product_name = models.CharField(max_length=255)

    def summ(self):
        return self.product_price * self.count

    def __str__(self):
        return self.user

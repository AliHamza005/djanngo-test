from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

class Promotion(models.Model):
    description = models.CharField(max_length=255,default=uuid4)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product_id = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')
    
    def __str__(self) -> str:
        return self.title
   
    class Meta:
        ordering = ['title']
#Product  Model
class Product(models.Model):
    title = models.CharField(max_length=255,null=False)
    slug = models.CharField(max_length=255,default='')    
    description = models.TextField(null=True,blank=True)
    unit_price = models.DecimalField(max_digits=6,
                                     decimal_places=2,
                                     validators=[MinValueValidator(5,message='Value should be greater than 5')])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,related_name='products')
    promotions = models.ManyToManyField(Promotion,null= True,blank= True)
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']
# Customer  Model
class Customer (models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_GOLD,'Gold'),
        (MEMBERSHIP_SILVER,'Silver')
    ]
    user= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_id')
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField (null=True)
    membership_choice = models.CharField(max_length = 1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    @admin.display(ordering='user__first_name')
    def first_name(self)->str:
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self)->str:
        return self.user.last_name
    class Meta:
        ordering = ['user__first_name','user__last_name']
# Order Class
class Order(models.Model):
    Pending = 'P'
    Complete = 'C'
    Failed = 'F'
    
    Payment_status = [
        (Pending,'Pending'),
        (Complete,'Completed'),
        (Failed,'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add = True)
    Payment_status = models.CharField(
        max_length = 1, choices=Payment_status, default=Pending)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,primary_key=True)
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)
    
class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
 
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()   

    class Meta:
        unique_together = [['cart','product']]
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
from django.db import models
from django.core.validators import MinValueValidator

class Promotion(models.Model):
    description = models.CharField(max_length=255)
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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField (null=True)
    membership_choice = models.CharField(max_length = 1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering = ['first_name','last_name']
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
    created_at = models.DateTimeField(auto_now_add=True)
 
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()   
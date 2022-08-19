from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField
from django.core.validators import MinValueValidator
from uuid import uuid4

# Create your models here.
#many to many relashion
#promotion --> product can be reveresed

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    descount=models.FloatField()

class Collection(models.Model):
    title=models.CharField(max_length=255)
    #circular depandency(we put the string in model)
    #to solve circular alarm add related name=+
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']
class Product(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    #maxdigit==max price decimalplaces=after ashar
    unit_price=models.DecimalField(max_digits=6,decimal_places=2,
    validators=[MinValueValidator(1,message="please choose between 1and greater")])
    inventory=models.IntegerField(validators=[MinValueValidator(1)])
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT)
    promotions=models.ManyToManyField(Promotion,blank=True)
    slug = models.SlugField(default='-')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']
    


class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'

    MEMBERSHIP_CHOICES =[

        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    
    
    ]

    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices= MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering=['last_name']

class Order(models.Model):

    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS__COMPLETE='C'
    PAYMENT_STATUS__FAILED='F'

    PAYMENT_STATUS__CHOICES =[

        (PAYMENT_STATUS_PENDING,'PENDING'),
        (PAYMENT_STATUS__COMPLETE,'COMPLETE'),
        (PAYMENT_STATUS__FAILED,'FAILED'),
    
    
    ]

    placed_at= models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS__CHOICES,default=PAYMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)


    


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)

#one to one relashioship
#each customer needs an adress so Customer is parent model and in ondelete=CASCADE say id parent delete child wich is the adrees must delete
#setting primary_key=True makes adress unique
#Foreginkey makes adrees non unique and each cutumer can have multiple adrress
class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.ForeignKey(Customer,on_delete=CASCADE)

class Cart(models.Model):
    #UUID from GUID(global Unique identifyer) in order not hackers access cart data
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at= models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.PositiveSmallIntegerField()

    class Meta:
        unique_together= [['cart','product']]


class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name= models.CharField(max_length=255)
    description=models.TextField()
    date=models.DateField(auto_now_add=True)





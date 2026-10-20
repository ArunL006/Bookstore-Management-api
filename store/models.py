from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    name=models.CharField(max_length=150)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,choices=[("customer","Customer"),("admin","Admin")],default="customer")
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username","name"]
    def __str__(self): return self.email

class Book(models.Model):
    title=models.CharField(max_length=250,db_index=True)
    authors=models.CharField(max_length=250)
    genre=models.CharField(max_length=100,db_index=True)
    isbn=models.CharField(max_length=20,unique=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal("0.01"))])
    description=models.TextField(blank=True)
    stock_quantity=models.PositiveIntegerField(default=0)
    image_url=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["title"]
    def __str__(self): return self.title

class Order(models.Model):
    STATUS=[("pending","Pending"),("shipped","Shipped"),("delivered","Delivered"),("cancelled","Cancelled")]
    PAYMENT=[("unpaid","Unpaid"),("paid","Paid"),("refunded","Refunded")]
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name="orders")
    status=models.CharField(max_length=20,choices=STATUS,default="pending")
    payment_status=models.CharField(max_length=20,choices=PAYMENT,default="unpaid")
    total_amount=models.DecimalField(max_digits=12,decimal_places=2,default=Decimal("0.00"))
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    book=models.ForeignKey(Book,on_delete=models.PROTECT,related_name="order_items")
    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)

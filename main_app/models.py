from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Custom User model with roles

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'
        CUSTOMER = 'customer', 'Customer'
        
    role = models.CharField(max_length=50, choices=Roles.choices, default=Roles.CUSTOMER)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

# Vendor model

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.vendor_name

# Item model

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default = 0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name
    
    
# Order and OrderItem models

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PREPARING = 'preparing', 'Preparing'
        DELIVERING = 'delivering', 'Delivering'
        COMPLETED = 'completed', 'Completed'
        CANCELED = 'canceled', 'Canceled'
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_by')
    handled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='handled_by')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id}"
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem {self.id} of Order {self.order_id.id}"
    

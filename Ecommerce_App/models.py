from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Categories(models.Model):
    Category=models.CharField(max_length=255,null=True)

class Products(models.Model):
    Category=models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
    Product_name=models.CharField(max_length=255,null=True)
    Description=models.CharField(max_length=255,null=True)
    Price=models.CharField(max_length=255,null=True)
    Product_image=models.ImageField(blank=True,upload_to="images/",null=True)

class Users(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Address=models.CharField(max_length=255,null=True)
    Contact_number=models.CharField(max_length=255,null=True)
    Image=models.ImageField(blank=True,upload_to="images/",null=True)

class Cart(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    Quantity = models.PositiveIntegerField(default=1)

    def Total_price(self):
        return float(self.Quantity) * float(self.Product.Price)

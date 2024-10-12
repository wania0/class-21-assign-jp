from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=15) 
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    price = models.FloatField()
    quantity = models.IntegerField()
    cat_id =  models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier_id = models.ManyToManyField(Supplier)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

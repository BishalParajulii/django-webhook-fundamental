from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
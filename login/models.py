from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128,null=False, blank=False)
    email = models.CharField(max_length=128,null=False, blank=False,unique=True)
    password = models.TextField(null=False, blank=False)
    
    def __str__(self):
        return self.name

class Retailer(models.Model):  
    first_name = models.CharField(max_length=128,null=False, blank=False)
    last_name = models.CharField(max_length=128,null=False, blank=False)
    company_name = models.CharField(max_length=128,null=False, blank=False)
    email = models.CharField(max_length=128,null=False, blank=False,unique=True)
    password = models.TextField(null=False, blank=False)
    gstNo = models.TextField(null=False, blank=False,unique=True)
    whyyou = models.TextField(null=False, blank=False)
    Products = models.TextField(null=False, blank=False) 

    def __str__(self):
        return self.Products
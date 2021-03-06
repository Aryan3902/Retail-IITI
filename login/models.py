from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128,null=False, blank=False)
    email = models.CharField(max_length=128,null=False, blank=False,unique=True)
    password = models.TextField(null=False, blank=False)
    gender = models.CharField(max_length=128, default="None")
    hostel = models.CharField(max_length=128, default="None")
    room = models.CharField(max_length=128, default="None")
    phone = models.CharField(max_length=128, default="None")
    
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
    Retailer_ID = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=datetime.now)
    phone = models.CharField(max_length=128, default="None")
    address = models.CharField(max_length=128, default="None")
    city = models.CharField(max_length=128, default="None")
    state = models.CharField(max_length=128, default="None")

    def __str__(self):
        return self.Retailer_ID.__str__()
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128,null=False, blank=False)
    email = models.CharField(max_length=128,null=False, blank=False,unique=True)
    password = models.TextField(null=False, blank=False)
    
    def __str__(self):
        return self.name
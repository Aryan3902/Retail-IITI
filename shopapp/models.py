from django.db import models
# form login.models import User
# from django.contrib.auth.models import User
from datetime import datetime
from login.models import User

# Create your models here.
class Product(models.Model):
    product_id = models.IntegerField(primary_key=True, null=False, blank=False)
    product_name = models.CharField(max_length=128,null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    company_name = models.CharField(max_length=128,null=False, blank=False)
    availability = models.CharField(max_length=128,null=False, blank=False)
    image = models.URLField(max_length=5000, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjw8YPUNzXPoROoi5DbrP2LEXL5Fs4txr3Aw&usqp=CAU")
    

    def __str__(self):
        return self.product_name



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=12345)

    # TAX_AMOUNT = 19.25

    # def price_ttc(self):
    #     return self.price_ht * (1 + TAX_AMOUNT/100.0)

    def __str__(self):
        return   self.cart.user.name + " - " + self.product.product_name 


class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)
    # cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=12345)


    def __str__(self):
        return  str(self.id) #self.user.name + " - " + self.product.product_name 
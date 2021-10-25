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

    # TAX_AMOUNT = 19.25

    # def price_ttc(self):
    #     return self.price_ht * (1 + TAX_AMOUNT/100.0)

    def __str__(self):
        return  self.cart.user.name + " - " + self.product.product_name
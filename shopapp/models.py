from django.db import models
from login.models import Retailer
# from django.contrib.auth.models import User
from datetime import datetime
from login.models import User, Retailer

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=128, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    company_name = models.CharField(max_length=128, null=False, blank=False)
    Quantity = models.IntegerField(default=0, blank=False)
    image = models.URLField(
        max_length=5000, default="https://bitsofco.de/content/images/2018/12/broken-1.png")
    Retailer_ID = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    availability = models.CharField(max_length=128, default="Out of Stock")

    def __str__(self):
        return self.product_name + " ( product id "+self.product_id.__str__()+" ) "+" by "+self.company_name


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
        return self.cart.user.name + " - " + self.product.product_name


class Orders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price_ht = models.FloatField(blank=True)
    # cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=12345)

    def __str__(self):
        # self.user.name + " - " + self.product.product_name
        return str(self.id)

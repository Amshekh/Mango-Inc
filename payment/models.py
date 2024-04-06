from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=175)
    shipping_email = models.EmailField(max_length=75)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200, blank=True, null=True)
    shipping_city = models.CharField(max_length=75)
    shipping_state = models.CharField(max_length=75, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=20, blank=True, null=True)
    shipping_country = models.CharField(max_length=125)

    class Meta:
        verbose_name_plural = "Shipping Address"   # To stop putting extra 's' while showing in django admin

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
def create_shipping(sender, instance, created, **kwargs):  # Creating a user shipping address automatically when the user registers
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)    
    

class Order(models.Model):  # Creating Order Model
   user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
   full_name = models.CharField(max_length=175)
   email = models.EmailField(max_length=75)
   shipping_address = models.TextField(max_length=15000) 
   amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
   date_ordered = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
       return f'Order - {str(self.id)}'
   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'
    
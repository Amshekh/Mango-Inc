from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):    # Customer Profile creation
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address1 = models.CharField(max_length=175, blank=True, null=True)
    address2 = models.CharField(max_length=175, blank=True, null=True)
    city = models.CharField(max_length=75, blank=True)
    state = models.CharField(max_length=75, blank=True, null=True)
    zipcode = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=75, blank=True, null=True)
    previous_cart = models.CharField(max_length=175, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):  # Creating user profile automatically when the user registers
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)  # Automating the default profile creation for a user at registration

class Category(models.Model):   # Product Category
    name = models.CharField(max_length=75)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'
    
class Customer(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    phone = models.CharField(max_length=15)   #  e.g. 1 (739) 45278
    email = models.EmailField(max_length=75)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Product(models.Model):
    name = models.CharField(max_length=75)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')

    # Sale - Products on sale
    is_sale = models.BooleanField(default = False)
    sale_price = models.DecimalField(default = 0, decimal_places=2, max_digits=7)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.TextField(max_length=300, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    date = models.DateField(default = datetime.datetime.today)
    status = models.BooleanField(default=False)

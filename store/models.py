from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, related_name = 'customer',null=True, blank=True, on_delete=models.CASCADE)   #CASCADE propagates the change to all related fields #user can only have one customer, and customer can only have one user
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def image_url(self):      #allows us to get no errors if there's no image for a particular product
        try:
            url = self.image.url
        except:
            url =''
        return url                
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)    #NULL only sets that value to null
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null= True)
    
    def __str__(self):
        return str(self.id)
    
    @property 
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        cart_total = sum([item.get_total for item in order_items])
        return cart_total
    
    @property 
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        cart_total = sum([item.quantity for item in order_items])
        return cart_total
    
    @property
    def shipping(self):
        shipping =False
        order_items = self.orderitem_set.all()
        for i in order_items:
            if i.product.digital == False:
                shipping = True
        return shipping
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price*self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) 
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    addresss = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.addresss
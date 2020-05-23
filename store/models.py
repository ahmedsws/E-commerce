from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=14, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    Gender = (
        ('m','Male'),
        ('f','Female')
    )

    Color = (
        ('bk','Black'),
        ('wh','White'),
        ('bl','Blue'),
        ('rd','Red'),
        ('yl','Yellow'),
        ('gr','Green'),
    )

    Season = (
        ('s','Summer'),
        ('w', 'Winter'),
    )

    Brand = (
        ('k','Koton'),
        ('lc','LC Waikiki'),
        ('hm','H&M'),
    )

    Size = (
        ('3m','0-3 M'),
        ('6m','3-6 M'),
        ('9m','6-9 M'),
        ('12m','12 M'),
        ('18m','18 M'),
        ('24m','24 M'),
        ('3y','2-3 Y'),
        ('4y','3-4 Y'),
        ('5y','4-5 Y'),
        ('6y','5-6 Y'),
        ('7y','6-7 Y'),
        ('8y','7-8 Y'),
        ('9y','8-9 Y'),
        ('10y','9-10 Y'),
        ('11y','10-11 Y'),
        ('12y','11-12 Y'),
    )

    

    title = models.CharField(max_length=200, null=True)
    details = models.TextField(null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    color = models.CharField(choices=Color,max_length=2)
    season = models.CharField(choices=Season,max_length=4)
    gender = models.CharField(choices=Gender, max_length=1)
    brand = models.CharField(choices=Brand,max_length=2)
    size = models.CharField(choices=Size,max_length=3)
    featured = models.BooleanField(default=False)
    category = models.CharField(max_length=200, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
   

class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

    def get_total_cart(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])
        return total
    
    def get_total_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    def get_total(self):
        total = self.product.price * self.quantity
        return int(total)
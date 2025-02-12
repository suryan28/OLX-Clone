from pyexpat import model
from sys import prefix
from unicodedata import category
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .managers import CustomUserManager
from django.utils import timezone



class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_choice=(('buyer','Buyer'),('seller','Seller'),)
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(blank=True, max_length=150, verbose_name='first name')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='last name')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(max_length=20, choices= user_choice , default='buyer')
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     if not self.is_superuser:
    #         self.set_password(self.password)
    #         self.save()
    #     return super(CustomUser, self).save(force_insert=False,
    #                                   force_update=False,
    #                                   using=None,
    #                                   update_fields=None)


class EmailVerifyOtp(models.Model):
    email = models.EmailField(max_length=50, null=True, blank=True)
    otp = models.CharField(max_length=10, blank=True, null=True)


class Category(models.Model):
    categories=models.CharField(max_length=50,null=True, blank=True)
        
    def __str__(self):
        return self.categories

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_categories=models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return self.sub_categories

        
class Product(models.Model):
   
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    product_title=models.CharField(max_length=150,null=True, blank=True)
    product_description=models.CharField(max_length=150,null=True, blank=True)
    product_price=models.CharField(max_length=150,null=True, blank=True)
    product_location=models.CharField(max_length=150,null=True, blank=True)
    image=models.ImageField(upload_to='product_img',null=True, blank=True)

    def __str__(self):
        return self.product_title

    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product_img',null=True, blank=True)

    def __str__(self):
        return self.product.product_title

class SubscriptionBase(models.Model):
    subscription_choice=(('monthly','Monthly'),('annual','Annual'),)
    subscription = models.CharField(max_length=20, choices= subscription_choice,null=True, blank=True  )
    days=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.subscription

class SubscriptionType(models.Model):
   # subscription_choice=(('monthly','Monthly'),('annual','Annual'),)
    name_choice=(('basic','Basic'),('standard','Standard'),('premium','Premium'))
   # subscription_name=  models.CharField(max_length=20, choices=  subscription_choice )
    package_name= models.CharField(max_length=20, choices= name_choice )
    price= models.FloatField(max_length=20, null=True, blank=True )
    ads_count=models.IntegerField(null=True, blank=True)
    subscription_name=models.ForeignKey(SubscriptionBase, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.package_name


class SubscriptionTransaction(models.Model):
    status_choice=(('initialized','Initialized'),('success','Success'),('failed','Failed')) 
    transaction_id=models.CharField(max_length=16,primary_key = True)
    amount= models.FloatField(max_length=20, null=True, blank=True )
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    transaction_status=models.CharField(max_length=20,choices=status_choice, default='initialized')
    invoice_id=models.CharField(max_length=16,null=True, blank=True)
    package=models.ForeignKey(SubscriptionType, on_delete=models.CASCADE,null=True)
    transaction_date=models.DateField(null=True,blank=True)

      

class UserSubscription(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    transaction=models.ForeignKey(SubscriptionTransaction,on_delete=models.CASCADE,null=True)
    purchase_date=models.DateField(null=True,blank=True)
    valid_till=models.DateField(null=True,blank=True)
    package=models.ForeignKey(SubscriptionType, on_delete=models.CASCADE,null=True)


class ChatRoom(models.Model):
    product_id=models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    buyer=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buyer',null=True)
    seller=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seller',null=True)


class ChatHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender',null=True)
    message=models.CharField(max_length=500,null=True,blank=True)
    receiver=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver',null=True)



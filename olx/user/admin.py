# import imp
from django.contrib import admin
from .models import Category, ChatHistory, ChatRoom,UserSubscription, CustomUser, EmailVerifyOtp, Product, ProductImage, Subcategory, SubscriptionBase, SubscriptionType,SubscriptionTransaction
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(EmailVerifyOtp)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Subcategory)
admin.site.register(SubscriptionBase)
admin.site.register(SubscriptionType)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionTransaction)
admin.site.register(ChatRoom)
admin.site.register(ChatHistory)










from datetime import datetime
from email.mime import image
from importlib.resources import Package
from multiprocessing import context
from unicodedata import category
from olx import settings
import user
from django.urls import reverse
from .models import  ChatHistory, CustomUser,UserSubscription, EmailVerifyOtp,Product,Category,ProductImage,Subcategory, SubscriptionBase,SubscriptionTransaction, SubscriptionType,ChatRoom
from django.http import HttpResponse, HttpResponseRedirect,request
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView,DeleteView
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth,User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.template import context
from .forms import ImageForm, InputForm, UpdateForm
from django.core.files.storage import FileSystemStorage
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
import uuid 
import string 
from django.db.models import Q
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

def home(request):
    """home page for olx"""
    if request.user.is_authenticated:
      productlist=Product.objects.exclude(owner=request.user)
    else:
        productlist=Product.objects.all()

    categorylist=Subcategory.objects.all()
    context={
       'productlist' : productlist,
       'categorylist' : categorylist,
    }
   
    return render(request, 'user/home.html', context)


def login(request):
   """view for user log in"""
   if request.method == 'POST':    
        e = request.POST['email']
        p = request.POST['password']
        print(e)
        user = auth.authenticate( email = e, password = p)
        if user is not None:
            auth.login(request, user)
            messages.success(request, ' wecome  !!')
            return redirect("/")
        else:
            messages.info(request, 'Invalid Email or Password')
            return render(request, 'login.html') 

   return render(request, 'login.html')

def generateOTP() :
    """for generating 6 digit otp"""
   
    return random.randint(000000,999999)


def send_otp(request):
    """sending generated otp to user"""
    p1=request.POST.get("p1")
    p2=request.POST.get("p2")
    email=request.POST.get("email")
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")

    if not p1==p2 :
        return redirect("/")
    
    if email == '':
      return redirect("/")
        
    otp=generateOTP()
    email_varification_obj = EmailVerifyOtp()
    email_varification_obj.email = email
    email_varification_obj.otp = otp
    email_varification_obj.save()
        
    subject = 'OTP request'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    message = f'your OTP is {otp}:'
    send_mail( subject, message, email_from, recipient_list )  
    return JsonResponse(otp,safe=False)


def signup(request):
   """Registration view for user"""
   if request.method == 'POST':
             
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
       
        context ={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password ' : password ,
        }
 
        if password==password1:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'email is already tken')
                return redirect('/signup')
            else:                              
            #    user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password)
            #    user.save()
            #    print ("user created")
               return redirect("/login")
                
        else:
             messages.error(request, 'password do not match')
             return redirect("/signup")
   
   return render(request, 'user/register.html') 


def logout(request):
    """Logout view"""
    auth.logout(request)
    return redirect("/")


def verify_otp(request):
    """OTP verification"""
    valid=False
    email_v=request.POST.get("email")
    otp=request.POST.get("otp")
    obj=EmailVerifyOtp.objects.filter(email=email_v).last()
    if obj.otp == otp:
        valid=True
        return JsonResponse(valid,safe=False)
    else:
        return JsonResponse(valid,safe=False)


def confirm_user(request):

    email=request.POST.get("email")
    first_name=request.POST.get("fname")
    last_name=request.POST.get("lname")
    password=request.POST.get("pwd")
    user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password)
    user.save()    
    return JsonResponse({'status': 'true'})


def forget_password(request):
   
   return render(request, 'user/forget_password.html') 


def setPassword(request):
    pwd1=request.POST.get("password1")
    pwd2=request.POST.get("password2")
    email=request.POST.get("email")
    if pwd1 == pwd2:
       user=CustomUser.objects.get(email = email)
       user.set_password(pwd1)
       user.save()
       return JsonResponse({'status': 'true'})
        
    return JsonResponse({'status': 'false'})



def reset(request):

    return render(request, 'user/reset.html')


def reset_password(request):
   if request.method == 'POST':
      pwd1=request.POST.get("password1")
      pwd2=request.POST.get("password2")
      current_password=request.POST.get("current_password")     
      current_email=request.POST.get("email")
      u = CustomUser.objects.get(email__exact=current_email)
      hashed_pass= u.password     
      if not pwd1==pwd2:
        return redirect("/")

      if (check_password(current_password,hashed_pass)) and (pwd1==pwd2):
            user=CustomUser.objects.get(email = current_email)
            user.set_password(pwd1)
            user.save()
            auth.logout(request)
            return JsonResponse({'status': 'true'})
          
        
def profile(request):
    
    product_by_user=Product.objects.filter(owner=request.user)
    chat_room=ChatRoom.objects.filter(seller_id=request.user.id)   

    context={
       'product_by_user' : product_by_user,
       'chat_room': chat_room,
    }
    return render(request, 'user/profile.html', context)


def setting(request):
    return render(request, 'user/setting.html')

   
def add_product(request):
    productlist=Product.objects.filter(owner=request.user)
    product_count=productlist.count()
    categorylist=Subcategory.objects.all()
    ImageFormSet = modelformset_factory(ProductImage,
                                        form=ImageForm, extra=3)

    form = InputForm(request.POST or None, request.FILES or None)
   
    if request.method =='POST':
          
        if form.is_valid():
            u=request.user
            subscribed_user= UserSubscription.objects.filter(user=u)
            expire= UserSubscription.objects.filter(user=u,valid_till__gt=datetime.now().date())
            product_limit= UserSubscription.objects.filter(user=u,valid_till__gt=datetime.now().date())
            
            if product_limit and product_count >= product_limit.package.ads_count:
                messages.error(request, 'Limit Reached for ads')
            if product_count >= 2 and not subscribed_user and not expire:
                 messages.error(request, 'Need subscription')
                 return redirect("/subscription")
         
            
            else:

               obj = form.save(commit = False)
               obj.owner = request.user
               obj.save()
              
               form = InputForm()
               context={
                  'form':form,
                  'categorylist':categorylist,
                  'productlist' :productlist,
                }
               return redirect('/',context)
          
  
    return render(request, 'add_product.html', {'form':form})
      

def product_by_category(request, pk):
    products=Product.objects.filter(category=pk)
    categorylist=Subcategory.objects.all()
    #categorylist=Category.objects.all()
    

    context={
       'products' : products,
       'categorylist' : categorylist,
    }
    return render(request, 'user/product_by_category.html', context)


class Delete_product(DeleteView):
    model=Product
    template_name = 'user/delete_product.html'
    success_url="/profile"


def detail_view(request, pk): 
   products=Product.objects.get(id=pk) 
   #print(products.owner.first_name)
   context={'products': products}
   return  render(request,"user/detail_view.html", context)


def update_product(request, pk):
    context ={}
    obj = get_object_or_404(Product, id = pk)
    products=Product.objects.get(id=pk)
    context ={'products': products}
    form = UpdateForm(request.POST or None, instance = obj)
    
    if form.is_valid():
        form.save()
        return  render(request,"user/profile.html", context)
 
   
    context["form"] = form
    return render(request, "update_product.html", context)

    
def room(request, user_id, room_name, sender_id):
    products=Product.objects.get(id=room_name) 
   
    buyer=CustomUser.objects.get(id=sender_id)
    seller=CustomUser.objects.get(id=user_id)
    c1 = Q(room__product_id=products.id)
    c2 = Q(room__buyer_id=buyer.id)
    #c3 = Q(room__seller=seller.id)

    chats=ChatHistory.objects.filter(c1 & c2 ).order_by('created_at')
    user=request.user


    ChatRoom.objects.get_or_create(product_id=products,buyer=buyer,seller=seller)
    
    return render(request, 'user/room.html', {
        'room_name': room_name,
        'products' : products,
        'chats': chats,
        'user': user,
        'buyer': buyer,
         'seller': seller,       

    })

def subscription(request):
    subscription_monthly=SubscriptionType.objects.filter(subscription_name__subscription ='monthly')
    subscription_annual=SubscriptionType.objects.filter(subscription_name__subscription ='annual')
    u=request.user
    subscribed_user= UserSubscription.objects.filter(user=u)
    valid= UserSubscription.objects.filter(user=u,valid_till__gt=datetime.now().date())
    if subscribed_user and  valid:
        subscribed_user= UserSubscription.objects.get(user=u)
        expire= UserSubscription.objects.get(user=u,valid_till__gt=datetime.now().date())
        d1=datetime.now().date()
        d2=expire.valid_till
        expiry_in=d2-d1
       

        context={
           'subscription_monthly': subscription_monthly,
           'subscription_annual': subscription_annual,
           'subscribed_user': subscribed_user,
           'expire': expire,
           'expiry_in': expiry_in       
        }
        return render(request, "user/subscription.html", context)  
    
    context={
        'subscription_monthly': subscription_monthly,
        'subscription_annual': subscription_annual,
        'subscribed_user': subscribed_user,
        # 'expire': expire,
        #'expiry_date': expiry_date
        # 'form': form,
    }
    return render(request, "user/subscription.html", context)

def subscription_process(request, pk):
    subscription_detail=SubscriptionType.objects.get(id= pk)
    invoice_number= 'Inv_'+str( ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)) )
    host = request.get_host()    
    package=subscription_detail.id
    amount=subscription_detail.price
    paypal_dict = {
      
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": subscription_detail.price,
        "item_name": subscription_detail.id,
        "invoice": str(invoice_number),
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('user:payment_done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('user:payment_cancelled')),
   
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context={
        'subscription_detail' : subscription_detail,
          'form': form,
    }
    
    #transaction(request,pk)
    
    transaction_id= 'Tnx_'+str( ''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)) )
    invoice_id=invoice_number
    amount=subscription_detail.price
    subscriber=request.user
    user=subscriber
    package=subscription_detail
    date=datetime.now()
    transaction=SubscriptionTransaction.objects.create(user=user,transaction_id=transaction_id,amount=amount, invoice_id= invoice_id, package=package,transaction_date=date)
    transaction.save()
   
    return render(request, "user/subscription_process.html", context)



def message(request):
    chat_room=ChatRoom.objects.filter(Q(seller_id=request.user.id) | Q(buyer_id=request.user.id)) 
       
    context={
      
    'chat_room': chat_room,
    }
    return render(request, "user/message.html", context)





    # def validate_email(request,):

#     que = request.GET.get('email_text', None)
#     data = {
#         'is_taken': CustomUser.objects.filter(email__iexact = que).exists()
#     }
#     return JsonResponse(data)

@csrf_exempt
def payment_done(request):
    return render(request, 'user/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'user/payment_cancelled.html')

def seller_profile(request, pk): 
    detail=CustomUser.objects.get(id=pk) 
    product_by_user=Product.objects.filter(owner_id=pk)

   #print(products.owner.first_name)
    context={
        'detail': detail,
        'product_by_user' : product_by_user,
        }
    return  render(request,"user/seller_profile.html", context)


def search_product(request):
    """ search function  """
    if request.method == "POST":
        
        query_name = request.POST.get('search', None)
        

        if query_name:
            categorylist=Subcategory.objects.all()
            productlist = Product.objects.filter(Q(product_title__contains=query_name) | Q(category__sub_categories__contains=query_name))
            # if request.user.is_authenticated:
            #     print('in')
            #     productlist = Product.objects.filter(Q(product_title__contains=query_name) | Q(category__sub_categories__contains=query_name))
            #     productlist=productlist.exclude(owner=request.user)
            # else:
            #     productlist = Product.objects.filter(product_title__contains=query_name)
            return render(request, 'search_product.html', {"productlist":productlist,'categorylist' : categorylist,})

    return render(request, 'search_product.html')
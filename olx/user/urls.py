from atexit import register
from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView

# importing views from views..py
app_name = 'user'
urlpatterns = [
    path('', views.home,name="home"),
    path('signup/',views.signup,name='signup'),   
    path('send_otp', views.send_otp, name='sendOTP' ),
    path('login/',views.login,name='login'),
    #path('signup/validate_email/', views.validate_email, name='validate_email'),
    path('logout/',views.logout,name='logout'),
    path('verify_otp', views.verify_otp, name='verify_otp' ),
    path('confirm_user', views.confirm_user, name='confirm_user' ),
    path('forget_password', views.forget_password, name='forget_password' ),
    path('setPassword', views.setPassword, name='setPassword' ),
    path('reset', views.reset, name='reset' ),
    path('reset_password', views.reset_password, name='reset_password' ),
    path('profile/', views.profile, name='profile' ),
    path('setting/', views.setting, name='setting' ),
    path('add_product/', views.add_product, name='add_product' ),
    path('product_by_category/<pk>', views.product_by_category,name="product_by_category"),
   # path('delete_product/<product_id>', views.delete_product.as_view(), name='delete_product' ),
    path('<pk>/delete_product', views.Delete_product.as_view(), name='delete_product' ),
    path('detail_view/<pk>', views.detail_view, name='detail_view' ),
    path('<pk>/update_product', views.update_product, name='update_product' ),
    path('<int:user_id>/<int:room_name>/<int:sender_id>/', views.room, name='room'),
  #  path('', views.index, name='index'),
    path('subscription', views.subscription, name='subscription' ),
    path('subscription_process/<pk>', views.subscription_process, name='subscription_process' ),
    path('message', views.message, name='message' ),
    path('payment_done/', views.payment_done,name='payment_done'),
    path('payment_cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('seller_profile/<pk>', views.seller_profile, name='seller_profile' ),
    #path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('search_product', views.search_product,name="search_product"),


    











   
] 
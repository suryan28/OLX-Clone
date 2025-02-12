from datetime import datetime, timedelta, timezone
from urllib import request
from django.shortcuts import get_object_or_404
from .models import SubscriptionTransaction,UserSubscription
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver



@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    print('reciver called')
    if ipn.payment_status == 'Completed':
        # payment was successful
       # order = get_object_or_404(SubscriptionTransaction, id=ipn.invoice)
        
        my_pk = ipn.invoice
        transaction_obj= SubscriptionTransaction.objects.get( invoice_id=my_pk)

        if transaction_obj.amount == ipn.mc_gross:
            
            transaction_obj.transaction_status = 'success'
            transaction_obj.save()
            duration=transaction_obj.package.subscription_name.days
            user=transaction_obj.user
            transaction=transaction_obj
            package=transaction_obj.package
            purchase_date=datetime.now()
            valid_till = datetime.now() + timedelta(days=duration)
            subscriber=UserSubscription.objects.create(user=user,transaction=transaction,package=package,valid_till=valid_till,purchase_date=purchase_date)
            subscriber.save()

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customers')
        instance.groups.add(group)                                      #Adding the user to the group

        Customer.objects.create(user=instance, name=instance.username)  #When a user is registered, a Customer is being registered at the same time
        print("Profile created !")

post_save.connect(customer_profile, sender=User)
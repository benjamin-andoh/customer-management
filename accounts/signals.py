# from django.db.models.signals import post_save
# from django.contrib.auth.models import User, Group
# from .models import Customer
#
#
# # for creating a new profile
# def customer_profile(sender, instance, create, **kwargs):
#     if create:
#         # user is the instance
#         group = Group.objects.get(name='customer')
#         instance.group.add(group)
#
#         Customer.objects.create(
#             user=instance,
#             name=instance.username,
#         )
#
#
# post_save.connect(customer_profile, sender=User)

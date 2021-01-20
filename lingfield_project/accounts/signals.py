from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, UserBirthDate, Dependent

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#         UserAddress.objects.create(user=instance)
#         UserInfo.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     instance.address.save()
#     instance.info.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_user_birthdate')
def save_birthdate(sender, instance, created, **kwargs):
    user = instance
    if created:
        birthdate = UserBirthDate(user=user)
        birthdate.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_user_dependent')
def save_dependent(sender, instance, created, **kwargs):
    user = instance
    if created:
        dependent = Dependent(user=user)
        dependent.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_surgery')
def save_surgery(sender, instance, created, **kwargs):
    user = instance
    if created:
        surgery = AddSurgery(user=user)
        surgery.save()

@receiver(post_save, sender=User, dispatch_uid='save_medicine')
def save_medicine_item(sender, instance, created, **kwargs):
    user = instance
    if created:
        item = MedicineItems(user=user)
        item.save()


# @receiver(post_save, sender=User, dispatch_uid='save_new_add_surgery')
# def save_add_surgery(sender, instance, created, **kwargs):
#     user = instance
#     if created:
#         add_surgery = AddSurgery(user=user)
#         add_surgery.save()
    
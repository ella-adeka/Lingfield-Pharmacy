from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, UserBirthDate, Dependent


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


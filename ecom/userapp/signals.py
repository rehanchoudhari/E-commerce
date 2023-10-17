from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProfileDetials, Location


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwarg):
    if created:
        ProfileDetials.objects.create(user=instance)

@receiver(post_save, sender=ProfileDetials)
def create_profile_address(sender, instance, created, **kwarg):
    if created:
        instance.location = Location.objects.create()
        instance.save()

@receiver(post_delete, sender=ProfileDetials)
def delete_location_of_user(sender, instance, *arg, **kwarg):
    if instance.location:
        instance.location.delete()

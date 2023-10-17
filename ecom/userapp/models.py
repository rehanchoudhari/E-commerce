from django.db import models
from django.contrib.auth.models import User
from .comman_utils import get_dirctory

# Create your models here.

class Location(models.Model):
    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=64, blank=True)

    def __str__(self) -> str:
        return f'Location {self.id}'


class ProfileDetials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=get_dirctory, null=True)
    bio = models.CharField(max_length=150, blank=True)
    mobile_no = models.CharField(max_length=12, blank=True)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'{self.user.username}\'s Profile'
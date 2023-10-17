from dataclasses import fields
from django import forms
from .models import Location, ProfileDetials
from django.contrib.auth.models import User
from .widgets import CustomeImagesForProfile


class LocationForm(forms.ModelForm):

    address_1 = forms.CharField(required=True)
    class Meta:
        model = Location
        fields = ('address_1', 'address_2', 'city', 'state', 'zip_code')
    

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        username = forms.CharField(disabled=True)
        fields = ('username', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):

    profile_pic = forms.ImageField(widget=CustomeImagesForProfile)
    
    class Meta:
        model = ProfileDetials
        fields = ('profile_pic', 'bio', 'mobile_no')

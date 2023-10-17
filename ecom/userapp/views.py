from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, ProfileForm, LocationForm
from main_sell.models import Listing, LikedListing

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        user_data = AuthenticationForm(request=request, data=request.POST)
        if user_data.is_valid():
            username = user_data.cleaned_data.get('username')
            password = user_data.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are now logged in as {username}')
                return redirect('home')
            else:
                messages.error(request, f'An error occured trying to login.{username}')
        else:
            messages.error(request, f'An error occured trying to login.')
    elif request.method == 'GET':
        user_data = AuthenticationForm()
    return render(request, 'html_views/login.html', {"login": user_data})

@login_required
def user_logout(request):
    logout(request)
    return redirect('main_page')


class RegisterView(View):

    def get(self, request):
        register_form = UserCreationForm()
        return render(request, 'html_views/register.html', {'register_form': register_form})
    
    def post(self, request):
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            password = register_form.cleaned_data.get('password')
            login(request, user)
            messages.error(request, f'User {user.username} register successfully.')
            return redirect('home')
        else:
            messages.error(request, f'An error Occured trying to register')
            return render(request, 'html_views/register.html', {'register_form': register_form})
        
@method_decorator(login_required, name='dispatch')
class ProfileView(View):

    def get(self, request):
        own_listing_data = Listing.objects.filter(seller=request.user.profiledetials)
        user_liked_listings = LikedListing.objects.filter(profile=request.user.profiledetials).all()
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profiledetials)
        location_form = LocationForm(instance=request.user.profiledetials.location)
        return render(request, 'html_views/profile.html', {'user_form': user_form,
                                                           'profile_form': profile_form,
                                                           'location_form': location_form,
                                                           'own_listing_data': own_listing_data,
                                                           'user_liked_listings': user_liked_listings})
    
    def post(self, request):
        own_listing_data = Listing.objects.filter(seller=request.user.profiledetials)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profiledetials)
        location_form = LocationForm(request.POST, instance=request.user.profiledetials.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile Detail Updated Successfully!')
        else:
            messages.error(request, 'Error Occured!')
        return render(request, 'html_views/profile.html', {'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'location_form': location_form,
                                                    'own_listing_data': own_listing_data})
from imp import reload
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Listing, LikedListing
from .forms import ListingForm
from userapp.forms import LocationForm
from django.contrib import messages
from .filters import ListingFilter
from userapp.forms import LocationForm
from django.shortcuts import get_object_or_404
# from main_sell.service import SellServices

# Create your views here.


# class FirstService(View):
    
#     def get(self, request):
#         # html_string = SellServices().get_html_string()
#         return HttpResponse("<h1> lets try with some other prints</h1>")


def main_page(request):
    return render(request, 'html_views/main_page.html', {'name': 'E-Sell-Buy'})

@login_required
def home_page(request):
    cars_data = Listing.objects.all()
    list_data = ListingFilter(request.GET, queryset=cars_data)
    user_liked_listing = LikedListing.objects.filter(profile=request.user.profiledetials).values_list('listing')
    user_liked_listing_ids = [l[0] for l in user_liked_listing]
    context = {
        'listing_filter': list_data,
        'user_liked_listing_ids': user_liked_listing_ids
    }
    return render(request, 'html_views/home_page.html', context)

@login_required
def list_page(request):
    if request.method == 'POST':
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profiledetials
                listing.location = listing_location
                listing.save()
                messages.info(request, f'{listing.model} Listing Posted Successfully!')
                return redirect('home')
            else:
                raise Exception('There is issue with provided data')
        except Exception as e:
            messages.info(request, 'An error occured while posting the listing.')
    elif request.method == 'GET':
        listing_form = ListingForm()
        location_form = LocationForm()
        return render(request, 'html_views/list.html', {'listing_form': listing_form, 'location_form': location_form})
    return render(request, 'html_views/list.html')

@login_required
def listing_views(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception()
        return render(request, 'html_views/listing.html', {'listing': listing})
    except Exception as e:
        messages.error(request, f'Invalid uid {id} was provided.')
        return redirect('home')
    

@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception()
        if request.method == 'POST':
            list_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = LocationForm(request.POST, instance=listing.location)
            if list_form.is_valid() and location_form.is_valid():
                list_form.save()
                location_form.save()
                messages.success(request, f'Changes are done for id:{id} please reload and check')
                return redirect('home')
            else:
                messages.error(request, f'error occured during update!')
                return reload()
        else:
            list_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
        return render(request, 'html_views/edit.html', {'list_form': list_form, 'location_form': location_form})
    except Exception as e:
        messages.error(request, 'Error Occured')
        return redirect('home')
    
@login_required
def liked_listing_view(request, id):
    print(id)
    listing = get_object_or_404(Listing, id=id)
    liked_listing, created = LikedListing.objects.get_or_create(profile=request.user.profiledetials, listing=listing)
    if not created:
        liked_listing.delete()
    else:
        liked_listing.save()

    return JsonResponse({
        'is_liked_by_user': created
    })
from django.urls import path
# from main_sell.views import FirstService
from .views import main_page, home_page, list_page, listing_views, edit_view, liked_listing_view

urlpatterns = [
    path('', main_page, name='main_page'),
    path('home/', home_page, name='home'),
    path('list/', list_page, name='list'),
    path('listing/<str:id>/', listing_views, name='listing'),
    path('listing/<str:id>/edit/', edit_view, name='edit'),
    path('listing/<str:id>/like/', liked_listing_view, name='like'),
]
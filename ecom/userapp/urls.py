from django.urls import path
from .views import login_page, RegisterView, user_logout, ProfileView

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_logout/', user_logout, name='user_logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
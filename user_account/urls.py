from django.urls import path
from user_account import views

urlpatterns = [
    path('<int:id>', views.profile, name='profile'),
    path('update', views.profile_update, name='profile_update'),
    path('favorite_clinics', views.favorite_clinics, name='favorite_clinics'),
    path('profile_inactive', views.profile_inactive, name='profile_inactive'),
]

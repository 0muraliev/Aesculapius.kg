from django.urls import path
from user_account import views

urlpatterns = [
    path('<int:id>', views.profile, name='profile'),
    path('update', views.profile_update, name='profile_update'),
]

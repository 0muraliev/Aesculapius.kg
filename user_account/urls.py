from django.urls import path
from user_account import views

urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
]

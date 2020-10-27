from django.urls import path
from user_account import views

urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('registration', views.registration, name='registration'),
    path('password_change', views.password_change, name='password_change'),
]

from django.urls import path

from . import views


urlpatterns = [
    path('profile/<int:id>', views.doctor_profile, name='doctor_profile'),
    path('profile/update', views.doctor_update, name='doctor_update'),
    path('signup', views.doctor_signup, name='doctor_signup'),
]

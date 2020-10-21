from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinics, name='clinics'),
    path('<int:id>', views.clinic, name='clinic'),
]

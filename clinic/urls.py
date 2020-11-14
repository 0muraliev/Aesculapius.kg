from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinics, name='clinics'),
    path('<slug:slug>-<int:id>', views.clinic, name='clinic'),
    path('department/<slug:slug>', views.departments, name='department'),
    path('department/<int:id>', views.departments)
]

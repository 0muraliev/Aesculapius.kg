from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinics, name='clinics'),
    path('<slug:slug>-<int:id>', views.clinic, name='clinic'),
    path('department', views.departments, name='departments'),
    path('department/<slug:slug>', views.department, name='department')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('appointment/<int:id>', views.make_appointment, name='appointment'),
]

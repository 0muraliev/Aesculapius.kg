from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('appointment/clinic/<int:id>', views.make_appointment_clinic, name='appointment_clinic'),
    path('appointment/doctor/<int:id>', views.make_appointment_doctor, name='appointment_doctor'),
    path('letter/clinic/<int:id>', views.letter_clinic, name='letter_clinic'),
    path('letter/doctor/<int:id>', views.letter_doctor, name='letter_doctor'),
]

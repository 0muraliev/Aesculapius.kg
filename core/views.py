from django.shortcuts import render

from user_account.models import Doctor


def home(request):
    doctors = Doctor.objects.filter(user__is_active=True)
    return render(request, 'core/home.html', {'doctors': doctors})

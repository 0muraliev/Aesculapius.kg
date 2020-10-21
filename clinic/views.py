from django.shortcuts import render
from .models import Clinic


def clinics(request):
    context = {'clinics': Clinic.objects.all()}
    return render(request, 'clinics.html', context)


def clinic(request, id):
    context = {'clinic': Clinic.objects.get(id=id)}
    return render(request, 'clinic.html', context)

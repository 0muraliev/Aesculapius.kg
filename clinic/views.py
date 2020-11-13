from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

from .forms import ReviewForm
from .models import Clinic, Review


def clinics(request):
    context = {'clinics': Clinic.objects.all()}
    return render(request, 'clinics.html', context)


def clinic(request, id):
    clinic = Clinic.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            clinic_review = form.save(commit=False)
            clinic_review.clinic = clinic
            clinic_review.user = request.user
            try:
                clinic_review.save()
            except IntegrityError:
                messages.error(request, 'Вы уже оставили свой отзыв:)')

            messages.success(request, 'Вы успешно оставили отзыв!')
            return redirect('clinic', id=clinic.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

    context = {}
    context['clinic'] = clinic
    context['reviews'] = Review.objects.filter(clinic__name=clinic)
    context['form'] = ReviewForm()
    return render(request, 'clinic.html', context)

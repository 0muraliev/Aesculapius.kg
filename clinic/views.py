from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import ReviewForm
from .models import Clinic, Review, MedicalDepartment


def clinics(request):
    """Страница всех клиник, а также поисковик"""
    if 'key' in request.GET:
        key = request.GET.get('key')
        # SQLite не поддерживает поиск без учета регистра
        clinics = Clinic.objects.filter(
            Q(name__icontains=key) |
            Q(medical_departments__name__icontains=key) |
            Q(address__icontains=key)
        ).distinct()
    else:
        clinics = Clinic.objects.all()

    """Пагинация страницы"""
    paginator = Paginator(clinics, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'clinics.html', {'clinics': clinics,
                                            'page_obj': page_obj})


def clinic(request, slug, id):
    """Все о клинике"""
    clinic = Clinic.objects.get(slug=slug, id=id)
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
            return redirect('clinic', slug=clinic.slug, id=id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

    context = {}
    context['clinic'] = clinic
    context['reviews'] = Review.objects.filter(clinic__name=clinic)
    context['form'] = ReviewForm()
    return render(request, 'clinic.html', context)


def departments(request):
    context = {'departments': MedicalDepartment.objects.order_by('name')}
    return render(request, 'departments.html', context)

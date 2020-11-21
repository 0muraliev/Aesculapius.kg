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
    return render(request, 'clinic/clinics.html', {'clinics': clinics,
                                                   'page_obj': page_obj})


def clinic(request, slug, id):
    """Все о клинике"""
    clinic = Clinic.objects.get(slug=slug, id=id)
    reviews = Review.objects.filter(clinic_id=clinic.id)
    review_user = request.user.reviews.filter(clinic_id=clinic.id)
    favorite_add_or_remove(request, clinic)
    if not review_user:
        return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                      'reviews': reviews,
                                                      'review_user': review_user,
                                                      'form_review': ReviewForm()})
    elif not reviews and not review_user:
        return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                      'form_review': ReviewForm()})
    else:
        return review_leave_or_change(request, clinic, reviews)


def review_leave_or_change(request, clinic, reviews):
    review = reviews.get(user_id=request.user.id)
    if 'review_leave' in request.POST:
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            clinic_review = form.save(commit=False)
            clinic_review.clinic = clinic
            try:
                clinic_review.user = request.user
                clinic_review.save()
                messages.success(request, 'Вы успешно оставили отзыв!')
            except IntegrityError:
                messages.info(request, 'Вы уже оставили свой отзыв:)')
            except ValueError:
                messages.info(request, 'Пожалуйста, убедитесь, что вы авторизованы.')
            return redirect('clinic', slug=clinic.slug, id=clinic.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

    elif 'review_change' in request.POST:
        form_change = ReviewForm(data=request.POST, instance=review)
        if form_change.is_valid():
            form_change.save()
            messages.info(request, 'Отзыв изменен.')
            return redirect('clinic', slug=clinic.slug, id=clinic.id)

    review_user = request.user.reviews.filter(clinic_id=clinic.id)
    form_review = ReviewForm()
    form_change = ReviewForm(instance=review)
    return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                  'reviews': reviews,
                                                  'review_user': review_user,
                                                  'form_review': form_review,
                                                  'form_review_change': form_change})


def favorite_add_or_remove(request, clinic):
    """
    Метод добавления/удаления клиники в/из Избранные
    """
    try:
        if 'favorite' in request.POST:
            clinic.favorite_clinics.add(request.user.profile)
            messages.info(request, 'Сохранено в избранные.')

        elif 'favorite_remove' in request.POST:
            clinic.favorite_clinics.remove(request.user.profile)
            messages.info(request, 'Удалено из избранных.')

    except AttributeError:
        messages.info(request, 'Чтобы сохранить клинику в Избранные, необходимо авторизоваться')


def departments(request):
    """Все медицинские отделения"""
    return render(request, 'clinic/departments.html',
                  {'departments': MedicalDepartment.objects.order_by('name')})


def department(request, slug):
    """Клиники связанные с медицинским отделением"""
    department_clinics = Clinic.objects.filter(medical_departments__slug=slug)
    department = MedicalDepartment.objects.get(slug=slug)
    return render(request, 'clinic/department-clinics.html',
                  {'department_clinics': department_clinics, 'department': department})

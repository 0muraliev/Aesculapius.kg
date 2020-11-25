from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import render, redirect

from communication.models import Appointment
from user_account.decorators import clinic_required
from user_account.forms import ClinicForm
from user_account.models import MedicalDepartment, Clinic
from .forms import ReviewForm, ClinicSignupForm
from .models import Review


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


@login_required
@clinic_required
def clinic_profile(request, id):
    clinic_profile = Clinic.objects.get(id=id)
    appointments = Appointment.objects.filter(clinic_id=id)
    return render(request, 'clinic/clinic_profile.html', {'clinic': clinic_profile,
                                                          'appointments': appointments})


@login_required
@transaction.atomic
def clinic_update(request):
    if request.method == 'POST':
        clinic_form = ClinicForm(data=request.POST, files=request.FILES, instance=request.user.clinic)
        if clinic_form.is_valid():
            clinic_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('clinic_profile', id=request.user.clinic.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')
    else:
        clinic_form = ClinicForm(instance=request.user.clinic)
    return render(request, 'clinic/clinic_update.html', {'clinic_form': clinic_form})


def clinic_signup(request):
    if request.method == 'POST':
        form = ClinicSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы зарегистрировали клинику! Пожалуйста, войдите.')
        else:
            messages.info(request, 'Пожалуйста, исправьте ошибку ниже.')

    form = ClinicSignupForm()
    return render(request, 'clinic/clinic_signup.html', {'clinic_signup': form})


def clinic(request, slug, id):
    """Все о клинике"""
    clinic = Clinic.objects.get(slug=slug, id=id)
    reviews = Review.objects.filter(clinic_id=clinic.id)
    favorite_add_or_remove(request, clinic)

    return review_leave_or_change(request, clinic, reviews)


def review_leave_or_change(request, clinic, reviews):
    if request.user.is_anonymous:
        context = {'clinic': clinic,
                   'reviews': reviews}
    elif not reviews and not request.user.reviews.filter(clinic_id=clinic.id):
        context = {'clinic': clinic,
                   'form_review': ReviewForm()}
    elif not request.user.reviews.filter(clinic_id=clinic.id):
        context = {'clinic': clinic,
                   'reviews': reviews,
                   'review_user': request.user.reviews.filter(clinic_id=clinic.id),
                   'form_review': ReviewForm()}
    else:
        context = {'clinic': clinic,
                   'reviews': reviews,
                   'review_user': request.user.reviews.filter(clinic_id=clinic.id),
                   'form_review': ReviewForm(),
                   'form_review_change': ReviewForm(instance=reviews.get(user_id=request.user.id))}

    if 'review_leave' in request.POST:
        form = ReviewForm(data=request.POST)
        if form.is_valid() and not request.user.is_clinic:
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

        elif request.user.clinic:
            messages.info(request, 'Чтобы оставить отзыв, авторизуйтесь через аккаунт профиля.')
        else:
            messages.info(request, 'Пожалуйста, исправьте ошибку ниже.')

    elif 'review_change' in request.POST:
        form_change = ReviewForm(data=request.POST, instance=reviews.get(user_id=request.user.id))
        if form_change.is_valid():
            form_change.save()
            messages.info(request, 'Отзыв изменен.')
            return redirect('clinic', slug=clinic.slug, id=clinic.id)

    return render(request, 'clinic/clinic.html', context)


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

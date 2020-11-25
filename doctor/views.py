from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from communication.models import Appointment
from doctor.forms import DoctorForm, DoctorSignupForm
from user_account.decorators import doctor_required
from user_account.forms import UserForm
from user_account.models import Doctor


@login_required
@doctor_required
def doctor_profile(request, id):
    doctor = Doctor.objects.get(id=id)
    appointments = Appointment.objects.filter(doctor_id=id)
    return render(request, 'doctor/doctor_profile.html', {'doctor': doctor,
                                                          'appointments': appointments})


@login_required
@transaction.atomic
def doctor_update(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        doctor_form = DoctorForm(data=request.POST, files=request.FILES, instance=request.user.doctor)
        if doctor_form.is_valid() and user_form.is_valid():
            user_form.save()
            doctor_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('doctor_profile', id=request.user.doctor.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')
    else:
        user_form = UserForm(instance=request.user)
        doctor_form = DoctorForm(instance=request.user.doctor)
    return render(request, 'doctor/doctor_update.html', {'user_form': user_form,
                                                         'doctor_form': doctor_form})


def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы зарегистрировались как доктор! Пожалуйста, войдите.')
        else:
            messages.info(request, 'Пожалуйста, исправьте ошибку ниже.')

    form = DoctorSignupForm()
    return render(request, 'doctor/doctor_signup.html', {'doctor_signup': form})

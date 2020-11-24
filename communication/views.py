from django.contrib import messages
from django.shortcuts import render, redirect

from clinic.models import Clinic
from .forms import MessageForm, AppointmentForm
from .models import Appointment


def contact(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            try:
                message.user = request.user
                message.email = request.user.email
                message.save()
                messages.success(request, 'Сообщение отправлено.')
            except AttributeError:
                messages.info(request, 'Чтобы отправить сообщение, пожалуйста, войдите в аккаунт.')

            return redirect('contact')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

    return render(request, 'communication/contact.html', {'form': MessageForm})


def make_appointment(request, id):
    clinic = Clinic.objects.get(id=id)
    profile = request.user.profile
    if request.method == 'POST':
        form = AppointmentForm(data=request.POST)
        if form.is_valid():
            appointment_form = Appointment(
                profile=profile,
                clinic=clinic,
                email=request.user.email,
                phone_number=form.cleaned_data['phone_number'],
                message=form.cleaned_data['message'],
                itn=profile.itn,
                birth_date=profile.birth_date,
                gender=profile.gender,
                blood_type=profile.blood_type
            )
            appointment_form.save()
            messages.success(request, 'Заявка отправлена. В течение 24 часов мы отправим Вам письмо в личный кабинет.')
        else:
            messages.info(request, 'Пожалуйста, проверьте правильность заполнения формы.')

    appointment_form = AppointmentForm()
    return render(request, 'communication/appointment.html', {'appointment_form': appointment_form,
                                                              'clinic': clinic})

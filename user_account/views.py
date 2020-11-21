from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect

from clinic.models import Clinic
from communication.models import Appointment
from .forms import UserForm, ProfileForm


@login_required
def profile(request, id):
    """
    Личный кабинет персонального пользователя.
    При попытке входа в чужой профиль, сервер переадресует пользователя на свой собственный.
    """
    user = User.objects.get(id=id)
    if request.user.id != user.id:
        return redirect('profile', id=request.user.id)

    appointments = Appointment.objects.filter(profile__user=user)
    return render(request, 'user_account/profile.html', {'user': user,
                                                         'appointments': appointments})


@login_required
@transaction.atomic
def profile_update(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, instance=request.user)
        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile', id=request.user.id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'user_account/profile_update.html', {'user_form': user_form,
                                                                'profile_form': profile_form})


@login_required
def favorite_clinics(request):
    context = {'favorite_clinics': Clinic.objects.filter(favorite_clinics=request.user.profile)}
    return render(request, 'user_account/favorite_clinics.html', context)


@login_required
def profile_inactive(request):
    """Метод деактивации/удаления аккаунта"""
    user = request.user
    user.is_active = False
    user.save()
    messages.info(request, """Вы успешно удалили аккаунт. Чтобы восстановить его, обратитесь в службу поддержки""")
    return redirect('home')

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect

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

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'user': user}
    return render(request, 'profile.html', context)


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
    return render(request, 'profile_update.html', {'user_form': user_form,
                                                   'profile_form': profile_form})

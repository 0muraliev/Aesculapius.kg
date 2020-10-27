from django.contrib import auth, messages
from django.contrib.auth import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from user_account.forms import RegistrationForm


def profile(request, id):
    """Личный кабинет персонального пользователя"""
    context = {'user': auth.models.User.objects.get(id=id)}
    return render(request, 'profile.html', context)


def login(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    if 'login' in request.POST:
        form = forms.AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('home')

    context = {'form': forms.AuthenticationForm()}
    return render(request, 'login.html', context)


def logout(request):
    """Выход из личного кабинета"""
    auth.logout(request)
    return redirect('home')


def registration(request):
    """Форма регистрации"""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login)

    context = {'form': RegistrationForm()}
    return render(request, 'registration.html', context)


@login_required
def password_change(request):
    """Изменение своего пароля пользователем"""
    user = request.user
    if request.user.id != user.id:
        return redirect('home')
    if request.method == 'POST':
        form = auth.forms.PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            auth.update_session_auth_hash(request, form.user)
            messages.success(request, 'Ваш пароль был успешно изменен.')
            return redirect('profile', id=user.id)
    else:
        form = auth.forms.PasswordChangeForm(user=request.user)

    return render(request, 'password_change_form.html', {'form': form})

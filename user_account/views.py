from django.contrib import auth
from django.shortcuts import render


def profile(request, id):
    """Личный кабинет персонального пользователя"""
    context = {'user': auth.models.User.objects.get(id=id)}
    return render(request, 'profile.html', context)

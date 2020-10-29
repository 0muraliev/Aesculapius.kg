from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


@login_required
def profile(request, id):
    """
    Личный кабинет персонального пользователя.
    При попытке входа в чужой профиль, сервер переадресует пользователя на свой собственный.
    """
    user = User.objects.get(id=id)
    if request.user.id != user.id:
        return redirect('profile', id=request.user.id)

    context = {'user': user}
    return render(request, 'profile.html', context)

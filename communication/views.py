from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import MessageForm


def contact(request):
    if request.method == 'POST':
        form = MessageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            try:
                message.profile = request.user.profile
                message.email = request.user.email
                message.save()
                messages.success(request, 'Сообщение отправлено.')
            except AttributeError:
                messages.info(request, 'Чтобы отправить сообщение, пожалуйста, войдите в аккаунт.')

            return redirect('contact')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

    return render(request, 'communication/contact.html', {'form': MessageForm})

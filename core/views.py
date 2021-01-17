from django.db.models import Q
from django.shortcuts import render

from user_account.models import Doctor


def home(request):
    """Главная страница."""
    # Для вывода доктора на главной странице,
    # необходимы активный статус доктора, биография и его имя или фамилия.
    doctors = Doctor.objects.filter(
        Q(user__is_active=True),
        ~Q(biography=''),
        ~Q(user__first_name='') |
        ~Q(user__last_name='')
    )
    return render(request, 'core/home.html', {'doctors': doctors})

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def profile_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
    """
    Декоратор для представлений, который проверяет, что вошедший в систему пользователь является обычным пользователем,
    при необходимости перенаправляет на Главную страницу.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_clinic,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)

    return actual_decorator


def clinic_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
    """
    Декоратор для представлений, который проверяет, что вошедший в систему пользователь имеет учетную запись клиники,
    при необходимости перенаправляет на Главную страницу.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_clinic,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

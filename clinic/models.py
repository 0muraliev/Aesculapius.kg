from django.db import models

from user_account.models import Clinic, User


class Review(models.Model):
    RATING_CHOICES = [
        (None, 'Оценить'),
        ('5', 'Отлично'),
        ('4', 'Хорошо'),
        ('3', 'Нормально'),
        ('2', 'Плохо'),
        ('1', 'Ужасно')
    ]
    rating = models.CharField('Оценка', max_length=1, choices=RATING_CHOICES)
    title = models.CharField('Название', max_length=50, blank=True)
    text = models.TextField('Отзыв(по желанию)', blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # Функция не дает повторно оставить отзыв
        constraints = [
            models.UniqueConstraint(fields=['user', 'clinic'], name='unique_review')
        ]
        # Сортировка по дате изменения по убыванию
        ordering = ['-updated']

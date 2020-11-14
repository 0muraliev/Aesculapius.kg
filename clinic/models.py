from django.contrib.auth.forms import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from location_field.models.plain import PlainLocationField


class Clinic(models.Model):
    name = models.CharField('Название', max_length=125)
    slug = models.SlugField(max_length=125, unique=True)
    information = models.TextField('Основная информация', blank=True)
    medical_departments = models.ManyToManyField('MedicalDepartment')
    image = models.ImageField('Изображение',
                              upload_to='clinics',
                              null=True,
                              blank=True)
    address = models.CharField('Адрес', max_length=255)
    location = PlainLocationField(based_fields=['address'], zoom=7, suffix='Bishkek')
    contact = models.CharField('Связаться с нами', max_length=45)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clinic', kwargs={'slug': self.slug, 'id': self.id})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class MedicalDepartment(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


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
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # функция не дает повторно оставить отзыв
        constraints = [
            models.UniqueConstraint(fields=['user', 'clinic'], name='unique_review')
        ]

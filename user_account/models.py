from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    is_clinic = models.BooleanField('clinic status', default=False)


class MedicalDepartment(models.Model):
    name = models.CharField(max_length=125)
    slug = models.SlugField(max_length=125, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('department', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Clinic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField('Название', max_length=125)
    slug = models.SlugField(max_length=125, unique=True)
    information = models.TextField('Основная информация', blank=True)
    medical_departments = models.ManyToManyField(MedicalDepartment, related_name='clinics')
    image = models.ImageField('Изображение',
                              upload_to='clinics',
                              null=True,
                              blank=True)
    address = models.CharField('Адрес', max_length=255)
    location = PlainLocationField(based_fields=['address'], zoom=7, suffix='Bishkek')
    contact = PhoneNumberField('Связаться с нами')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clinic', kwargs={'slug': self.slug, 'id': self.id})

    # Преобразует название клиники в URL-адрес
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Profile(models.Model):
    GENDER_CHOICES = [
        (None, 'Не указан'),
        ('М', 'Мужчина'),
        ('Ж', 'Женщина')
    ]
    CITY_CHOICES = [
        (None, 'Не указан'),
        ('БК', 'Бишкек'),
        ('Ош', 'Ош'),
        ('ДА', 'Джалал-Абад'),
        ('ТК', 'Токмок'),
        ('ТС', 'Талас'),
        ('КЛ', 'Каракол'),
        ('НН', 'Нарын'),
        ('БН', 'Баткен')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_clinic = models.ManyToManyField(Clinic,
                                             related_name='favorite_clinics',
                                             verbose_name='Избранные клиники',
                                             blank=True)
    phone_number = PhoneNumberField('Номер телефона', blank=True)
    itn = models.CharField('ИНН',
                           unique=True,
                           max_length=14,
                           validators=[
                               RegexValidator(regex='^\d{14}$',
                                              message='ИНН должен состоять из 14 цифр',
                                              code='nomatch')],
                           null=True,
                           blank=True)
    gender = models.CharField('Пол',
                              choices=GENDER_CHOICES,
                              max_length=1,
                              blank=True)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    city = models.CharField('Город',
                            choices=CITY_CHOICES,
                            max_length=2,
                            blank=True)
    blood_type = models.CharField('Группа крови', max_length=30, blank=True)
    photo = models.ImageField('Фото', upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Определение сигналов, чтобы модель Profile автоматически обновлялась при создании/изменении данных модели User.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

from django.db import models


class Clinic(models.Model):
    name = models.CharField('Название', max_length=125)
    information = models.TextField('Основная информация', blank=True)
    medical_departments = models.ManyToManyField('MedicalDepartment')
    image = models.ImageField('Изображение',
                              upload_to='clinics',
                              null=True,
                              blank=True)
    address = models.CharField('Адрес', max_length=125)
    contact = models.CharField('Связаться с нами', max_length=45)

    def __str__(self):
        return self.name


class MedicalDepartment(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name

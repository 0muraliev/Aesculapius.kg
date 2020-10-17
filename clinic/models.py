from django.db import models


class Clinic(models.Model):
    name = models.CharField('Название', max_length=125)
    information = models.TextField('Основная информация', blank=True)
    medical_departments = models.ManyToManyField('MedicalDepartment', )
    address = models.CharField('Адрес', max_length=125)
    contact = models.IntegerField('Связаться с нами', max_length=125)

    def __str__(self):
        return self.name


class MedicalDepartment(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name

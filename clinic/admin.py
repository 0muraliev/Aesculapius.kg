from django.contrib import admin

from user_account.models import MedicalDepartment
from .models import Clinic, Review


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    model = Clinic
    list_display = ('user', 'name', 'address', 'id')
    # Автозаполнение slug при именовании клиники
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MedicalDepartment)
class MedicalDepartmentsAdmin(admin.ModelAdmin):
    model = MedicalDepartment
    list_display = ('name', 'id')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('rating', 'title', 'clinic', 'user', 'created', 'updated')
    ordering = ['-updated']

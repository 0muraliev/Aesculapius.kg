from django.contrib import admin
from .models import Clinic, MedicalDepartment, Review


class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'id')
    # Автозаполнение slug при именовании клиники
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Clinic, ClinicAdmin)
admin.site.register(MedicalDepartment)
admin.site.register(Review)

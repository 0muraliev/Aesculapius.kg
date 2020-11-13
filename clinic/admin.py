from django.contrib import admin
from .models import Clinic, MedicalDepartment, Review


admin.site.register(Clinic)
admin.site.register(MedicalDepartment)
admin.site.register(Review)

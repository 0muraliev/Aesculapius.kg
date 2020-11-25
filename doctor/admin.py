from django.contrib import admin

from user_account.models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    model = Doctor
    list_display = ('user', 'clinic', 'id')

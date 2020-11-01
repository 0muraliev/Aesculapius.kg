from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'itn', 'gender', 'birth_date', 'city', 'blood_type', 'photo']


admin.site.register(Profile, ProfileAdmin)

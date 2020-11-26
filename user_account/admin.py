from django.contrib import admin
from .models import Profile, User


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'itn', 'gender', 'birth_date', 'city', 'blood_type', 'photo']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username', 'is_clinic', 'is_doctor', 'is_active', 'id']

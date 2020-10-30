from django import forms
from .models import User, Profile


class UserProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('itn', 'gender', 'birth_date', 'city', 'blood_type', 'photo')

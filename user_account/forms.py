from django import forms

from .models import User, Profile, Clinic


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'photo', 'itn', 'gender', 'birth_date', 'city', 'blood_type')
        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(1940, 2021)),
            'gender': forms.RadioSelect,
            'phone_number': forms.TextInput(attrs={'placeholder': '+996 XXX XXXXXX'})
        }


class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ('name', 'image', 'information', 'medical_departments', 'contact', 'address',)
        widgets = {
            'contact': forms.TextInput(attrs={'placeholder': '+996 XXX XXXXXX'})
        }

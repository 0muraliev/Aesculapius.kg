from django import forms

from .models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'itn', 'gender', 'birth_date', 'city', 'blood_type')
        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(1940, 2021)),
            'gender': forms.RadioSelect,
        }

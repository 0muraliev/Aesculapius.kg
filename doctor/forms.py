from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from user_account.models import Doctor, User


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['photo', 'clinic', 'specialization', 'biography']
        widgets = {
            'specialization': forms.SelectMultiple(attrs={'style': 'height: 250px;'}),
        }


class DoctorSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super(DoctorSignupForm, self).save(commit=False)
        user.is_doctor = True
        user.email = self.cleaned_data['email']
        user.save()
        return user

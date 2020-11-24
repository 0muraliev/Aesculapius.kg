from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from user_account.models import User, Clinic
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'title', 'text',)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'text-info'})


class ClinicSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    @transaction.atomic
    def save(self):
        user = super(ClinicSignupForm, self).save(commit=False)
        user.is_clinic = True
        user.email = self.cleaned_data['email']
        user.save()
        Clinic.objects.create(user=user, name=user.username)
        return user

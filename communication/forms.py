from django import forms

from .models import Message, Appointment


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['image', 'message_subject', 'message']
        widgets = {
                    'message_subject': forms.TextInput(attrs={'placeholder': 'Нет адреса клиники'}),
                    'message': forms.Textarea(
                        attrs={'placeholder': 'Пожалуйста, опишите свою идею как можно подробнее...'})
                }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['message']

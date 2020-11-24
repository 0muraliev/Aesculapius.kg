from django import forms

from .models import Message, Appointment, Letter


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
        fields = ['phone_number', 'message']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+996550050560'}),
            'message': forms.Textarea(
                attrs={'placeholder': 'Напишите, к какому специалисту Вы хотите записаться.'}
            )
        }


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['answer']
        widgets = {
            'answer': forms.Textarea(
                attrs={'placeholder': 'Отправить письмо',
                       'style': 'resize:none; width:auto; height: 150px;'},
            )
        }

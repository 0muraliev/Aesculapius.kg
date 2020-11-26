from django.contrib import admin

from .models import Message, Appointment, Letter


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['user', 'email', 'message_subject', 'date', 'id']


@admin.register(Appointment)
class MessageAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ['profile', 'clinic', 'doctor', 'email', 'phone_number', 'date']


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    model = Letter
    list_display = ['appointment', 'answer', 'id']

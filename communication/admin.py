from django.contrib import admin

from .models import Message, Appointment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['profile', 'email', 'message_subject', 'date', 'id']


@admin.register(Appointment)
class MessageAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ['profile', 'clinic', 'email', 'phone_number', 'date']

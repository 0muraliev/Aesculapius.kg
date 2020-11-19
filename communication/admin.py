from django.contrib import admin
from django.contrib.auth.forms import User

from .models import Message, Profile, Appointment


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['profile', 'email', 'message_subject', 'date', 'id']


@admin.register(Appointment)
class MessageAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = ['message']

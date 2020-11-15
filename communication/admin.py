from django.contrib import admin
from django.contrib.auth.forms import User

from .models import Message, Profile


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['profile', 'email', 'message_subject', 'date', 'id']

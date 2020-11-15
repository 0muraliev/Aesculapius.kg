from django.contrib.auth.models import User
from django.db import models

from user_account.models import Profile


class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    email = models.EmailField(User.get_email_field_name(), null=True, blank=True)
    image = models.ImageField('Приложить фотографию(по желанию)', upload_to='messages', blank=True)
    message_subject = models.CharField('Тема сообщения', max_length=80)
    message = models.TextField('Подробнее')
    date = models.DateTimeField('Дата обращения', auto_now_add=True)

    def __str__(self):
        return 'Message from {}'.format(self.profile.user.username)

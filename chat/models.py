from django.db import models
from accounts.models import NewUser

class Message(models.Model):
    sender = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    @staticmethod
    def get_all_messages(user_1, user_2):
        messages = Message.objects.filter(sender=user_1, recipient=user_2) | Message.objects.filter(sender=user_2, recipient=user_1)
        messages = messages.order_by('date')
        return messages

    @staticmethod
    def get_message_list(user):
        messages = Message.objects.filter(sender=user) | Message.objects.filter(recipient=user)
        user_list = set()
        message_list = []
        for message in messages:
            if message.sender == user:
                other_user = message.recipient
            else:
                other_user = message.sender

            if other_user not in user_list:
                user_list.add(other_user)
                message_list.append(message)
        message_list.sort(key=lambda x: x.date, reverse=True)
        return message_list

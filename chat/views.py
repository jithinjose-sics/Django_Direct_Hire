from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import NewUser
from .models import Message  # Assuming your Message model is in the same app

class MessagesListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messages_list.html'
    login_url = '/login2/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = NewUser.objects.get(pk=self.request.user.pk)
        messages = Message.get_message_list(user)
        other_users = []

        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        context['messages_list'] = messages
        context['other_users'] = other_users
        context['you'] = user
        return context


class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'inbox.html'
    login_url = '/login2/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(NewUser, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = NewUser.objects.get(pk=self.request.user.pk)
        other_user = self.get_object()
        messages = Message.get_message_list(user)
        other_users = []

        for i in range(len(messages)):
            if messages[i].sender != user:
                other_users.append(messages[i].sender)
            else:
                other_users.append(messages[i].recipient)

        sender = other_user
        recipient = user

        context['messages'] = Message.get_all_messages(sender, recipient)
        context['messages_list'] = messages
        context['other_person'] = other_user
        context['you'] = user
        context['other_users'] = other_users
        return context

    def post(self, request, *args, **kwargs):
        sender = NewUser.objects.get(pk=request.POST.get('you'))
        recipient = NewUser.objects.get(pk=request.POST.get('recipient'))
        message = request.POST.get('message')

        if message and request.method == 'POST':
            Message.objects.create(sender=sender, recipient=recipient, message=message)

        return redirect('chat:inbox', username=recipient.username)


class UserListsView(LoginRequiredMixin, ListView):
    model = NewUser
    template_name = 'users_list.html'
    context_object_name = 'users'
    login_url = '/login2/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = NewUser.objects.get(pk=self.request.user.pk)
        context['users'] = NewUser.objects.exclude(pk=user.pk)
        return context


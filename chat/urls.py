from django.urls import path
from .views import InboxView, MessagesListView, UserListsView  

app_name = 'chat'

urlpatterns = [
    path('', MessagesListView.as_view(), name='messages_list'),
    path('messages/', MessagesListView.as_view(), name='messages_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
    path('users/', UserListsView.as_view(), name='users_list'),
]

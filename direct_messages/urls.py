from django.urls import path
from . import views

app_name = 'direct_messages'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<str:username>/', views.conversation_detail, name='conversation_detail'),
    path('send/', views.send_message, name='send_message'),
]
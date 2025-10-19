from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_read'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
] 
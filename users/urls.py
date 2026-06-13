from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, views_settings

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    path('profile/<str:username>/block/', views.block_user, name='block_user'),
    path('profile/<str:username>/unblock/', views.unblock_user, name='unblock_user'),
    path('blocked/', views.blocked_users_list, name='blocked_users_list'),
    path('follow-requests/', views.follow_requests, name='follow_requests'),
    path('follow-requests/<int:request_id>/accept/', views.accept_follow_request, name='accept_follow_request'),
    path('follow-requests/<int:request_id>/reject/', views.reject_follow_request, name='reject_follow_request'),
    path('settings/', views_settings.settings_view, name='settings'),
    path('settings/password/', views_settings.UserPasswordChangeView.as_view(), name='password_change'),
    path('settings/email/', views_settings.change_email, name='change_email'),
    path('settings/delete/', views_settings.delete_account, name='delete_account'),
]
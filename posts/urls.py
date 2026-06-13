from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
     path('', views.post_list, name='post_list'),
     path('create/', views.post_create, name='post_create'),
     path('<int:post_id>/', views.post_detail, name='post_detail'),
     path('<int:post_id>/edit/', views.post_edit, name='post_edit'),
     path('<int:post_id>/delete/', views.post_delete, name='post_delete'),
     path('<int:post_id>/react/', views.react_to_post, name='react_to_post'),
     path('search/', views.search, name='search'),
     path('stories/', views.stories_list, name='stories_list'),
     path('stories/create/', views.create_story, name='create_story'),
     path('stories/<int:story_id>/', views.view_story, name='view_story'),
      path('api/posts/', views.api_post_list, name='api_post_list'),
      path('hashtag/<str:hashtag_name>/', views.hashtag_posts, name='hashtag_posts'),
      path('trending/', views.trending_hashtags, name='trending_hashtags'),
  ]
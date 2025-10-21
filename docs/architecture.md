# Architecture

This document describes the architecture of the Social Media Platform.

## Overview

The application follows a traditional Django web application structure with multiple apps that handle different features.

## Project Structure

```
socialmedia-app/
├── socialmediaproject/          # Django project settings
│   ├── settings.py              # Main settings file
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI application
│   └── asgi.py                  # ASGI application (for WebSocket support)
├── posts/                       # Posts functionality
│   ├── models.py                # Post, Comment, Reaction models
│   ├── views.py                 # Post-related views
│   ├── forms.py                 # Post forms
│   ├── urls.py                  # Post URLs
│   ├── serializers.py           # API serializers
│   └── utils.py                 # Utility functions
├── users/                       # User management
├── notifications/              # Notification system
├── direct_messages/            # Direct messaging
├── reports/                    # Content reporting
├── searchapp/                  # Search functionality
├── middleware/                 # Custom middleware
├── static/                     # Static files (CSS, JS, images)
├── templates/                  # HTML templates
├── media/                      # User uploads (images, videos)
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── README.md                   # Project README
```

## Core Apps

### 1. Posts App
- Handles post creation, editing, and deletion
- Manages comments and reactions
- Supports image and video uploads
- Implements hashtag functionality

### 2. Users App
- User registration and authentication
- Profile management
- User relationships (following/followers)

### 3. Notifications App
- Real-time notification system
- Activity tracking
- User notification preferences

### 4. Direct Messages App
- Private messaging between users
- Message history
- Online status tracking

## Database Schema

### Key Models

#### Post Model
- `author` (ForeignKey to User)
- `content` (TextField)
- `image` (ImageField, optional)
- `video` (FileField, optional)
- `hashtags` (ManyToMany to Hashtag)
- `created_at`, `updated_at` (DateTimeField)

#### User/Profile Model
- User authentication fields
- Profile information (bio, location, birth_date)
- Profile picture
- Following/follower relationships

#### Comment Model
- `post` (ForeignKey to Post)
- `author` (ForeignKey to User)
- `content` (TextField)
- `parent` (ForeignKey to self for nested comments)

## Technology Stack

- **Backend**: Django (Python web framework)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Caching**: Redis
- **Authentication**: Django built-in
- **File Storage**: Local (development) / Cloud (production)
- **Background Tasks**: django-background-tasks
- **WebSocket**: Django Channels (for notifications)

## Security Features

- Input validation and sanitization
- CSRF protection
- Rate limiting to prevent abuse
- File upload validation
- Proper authentication and authorization
- Secure session management

## Performance Considerations

- Database query optimization
- Redis caching for frequently accessed data
- Background task processing
- Pagination for content lists
- Static file optimization with Whitenoise
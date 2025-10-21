# Social Media Platform

A comprehensive social media application built with Django, featuring posts, stories, reactions, comments, and user interactions.

## 🚀 Features

- **User Authentication & Profiles**: Secure user registration, login, and profile management
- **Posts & Stories**: Share text, images, and videos with rich content creation
- **Reactions System**: Like, love, laugh, angry, and sad reactions to posts
- **Comments & Replies**: Threaded commenting system with nested replies
- **Hashtag Support**: Discover content through hashtag-based search
- **User Following**: Follow and unfollow other users
- **Notifications**: Real-time activity notifications
- **Rate Limiting**: Built-in protection against spam and abuse
- **File Upload Validation**: Secure image and video upload validation
- **Internationalization**: Multi-language support (English & Arabic)

## 🛠️ Tech Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (recommended for production), SQLite (development)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Authentication**: Django built-in authentication system
- **File Storage**: Local storage (configurable for cloud storage)
- **Caching**: Redis
- **Real-time**: Django Channels (for notifications)
- **Rate Limiting**: django-ratelimit

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- PostgreSQL (for production) / SQLite (for development)
- Redis (for caching)
- Pillow (for image processing)

## 🚀 Getting Started

### Prerequisites

```bash
# Install Python 3.8+ and pip
# Install Redis server
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd socialmedia-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=socialmedia_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Production Settings

For production deployment:

1. Set `DEBUG=False`
2. Use PostgreSQL instead of SQLite
3. Configure Redis for caching and sessions
4. Set up proper file storage (AWS S3, etc.)
5. Add security headers and HTTPS

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Run specific app tests:

```bash
python manage.py test posts
python manage.py test users
```

## 📊 API Endpoints

- `GET /api/posts/` - Get all posts
- `POST /api/posts/` - Create a new post
- `POST /posts/reactions/<post_id>/` - Add/remove reactions to posts
- `POST /comments/<post_id>/` - Add comments to posts
- `GET /search/` - Search posts and users

## 🔐 Security Features

- **Rate Limiting**: Prevents spam and abuse
- **File Upload Validation**: Secure file type and size validation
- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: ORM-based queries
- **XSS Prevention**: Automatic escaping in templates

## 📁 Project Structure

```
socialmedia-app/
├── socialmediaproject/          # Django project settings
├── posts/                       # Posts application
│   ├── models.py                # Post, Comment, Reaction models
│   ├── views.py                 # View logic for posts
│   ├── forms.py                 # Forms for posts
│   └── ...
├── users/                       # User management
├── notifications/              # Notification system
├── middleware/                 # Custom middleware
├── static/                     # Static files
├── templates/                  # HTML templates
├── media/                      # User uploads
├── requirements.txt            # Dependencies
├── manage.py                   # Django management script
└── README.md
```

## 🚀 Deployment

### Heroku Deployment

1. Create a Heroku app
2. Add PostgreSQL and Redis addons
3. Configure environment variables
4. Deploy using git

### Docker Deployment

Coming soon...

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`python manage.py test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any issues, please open an issue on GitHub with detailed information about the problem.

## 🙏 Acknowledgments

- Django Framework
- Bootstrap CSS
- django-ratelimit
- Pillow
- PostgreSQL
# Deployment

This guide covers deploying the Social Media Platform to production.

## Prerequisites

- Server with Python 3.8+
- PostgreSQL database
- Redis server
- Nginx (or equivalent reverse proxy)
- Gunicorn (or equivalent WSGI server)

## Production Setup

### 1. Environment Configuration

Create a production environment file with proper security settings:

```env
SECRET_KEY=your-long-and-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST_USER=your-smtp-user
EMAIL_HOST_PASSWORD=your-smtp-password
```

### 2. Database Setup

```bash
# Install PostgreSQL client
sudo apt-get install postgresql-client

# Create database and user
CREATE DATABASE socialmedia_db;
CREATE USER socialmedia_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE socialmedia_db TO socialmedia_user;
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate --settings=socialmediaproject.settings_production
```

### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## Production Server Setup

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn socialmediaproject.wsgi:application --bind 0.0.0.0:8000
```

### Nginx Configuration

Create an Nginx configuration file:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }
    
    location /media/ {
        root /path/to/your/project;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

## Deployment Configuration

### Production Settings

Create a production settings file if needed (e.g., `settings_production.py`):

```python
from .settings import *

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Production database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Redis settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
```

## Monitoring and Maintenance

### Logging

Ensure proper logging is configured for production:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/path/to/your/logfile.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Backup Strategy

Regularly backup:
- Database
- Media files
- Configuration files

### Security Updates

- Keep Django and dependencies updated
- Regular security audits
- Monitor for vulnerabilities
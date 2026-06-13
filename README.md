<div align="center">
  <img src="https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 5.1"/>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12"/>
  <img src="https://img.shields.io/badge/Channels-4.0-46BD84?style=for-the-badge&logo=django&logoColor=white" alt="Channels 4.0"/>
  <img src="https://img.shields.io/badge/DRF-3.14-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="DRF 3.14"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Ready"/>
  <br/>
  <img src="https://img.shields.io/github/actions/workflow/status/neoastra303/socialmedia-app/tests.yml?branch=main&style=flat-square&label=CI%2FCD" alt="CI/CD"/>
  <img src="https://img.shields.io/github/last-commit/neoastra303/socialmedia-app?style=flat-square" alt="Last Commit"/>
  <img src="https://img.shields.io/github/repo-size/neoastra303/socialmedia-app?style=flat-square" alt="Repo Size"/>
  <img src="https://img.shields.io/badge/tests-39%20passing-brightgreen?style=flat-square" alt="Tests 39 Passing"/>
  <img src="https://img.shields.io/badge/code%20style-black-000000?style=flat-square" alt="Code Style Black"/>
  <img src="https://img.shields.io/badge/i18n-Arabic%20%7C%20English-blue?style=flat-square" alt="i18n"/>
</div>

<h1 align="center">🚀— Social Media Platform</h1>

<p align="center">
  <b>A production-ready social media application built with Django 5.1</b><br/>
  Features real-time chat, stories, reactions, notifications, and a comprehensive REST API.<br/>
  Fully dockerized with CI/CD, comprehensive testing, and multi-language support.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#demo">Demo</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#api">API</a> •
  <a href="#testing">Testing</a> •
  <a href="#deployment">Deployment</a>
</p>

---

## ✨ Features

### 👤 User System

| Feature                                 | Status |
| --------------------------------------- | ------ |
| Registration with email verification    | ✅     |
| Login via email or username             | ✅     |
| JWT-ready authentication                | ✅     |
| Password reset flow (email-based)       | ✅     |
| Profile management with avatar upload   | ✅     |
| Account deletion                        | ✅     |
| Email change with password confirmation | ✅     |

### 📱 Social Features

| Feature                             | Status |
| ----------------------------------- | ------ |
| Text posts with image/video upload  | ✅     |
| Story sharing (24h auto-expiry)     | ✅     |
| 5-type reaction system (👍❤️😂😠😢) | ✅     |
| Threaded comments with replies      | ✅     |
| @mention and #hashtag auto-linking  | ✅     |
| Trending hashtags                   | ✅     |
| Post bookmarking / saved posts      | ✅     |
| Post search (content + hashtags)    | ✅     |

### 🔗 Social Graph

| Feature                                    | Status |
| ------------------------------------------ | ------ |
| Follow/unfollow users                      | ✅     |
| Private accounts (follow request approval) | ✅     |
| User blocking (auto-unfollows)             | ✅     |
| Followers/following lists                  | ✅     |

### 💬 Real-time Communication

| Feature                               | Status |
| ------------------------------------- | ------ |
| WebSocket-powered direct messaging    | ✅     |
| Real-time notification delivery       | ✅     |
| Instant message delivery via Channels | ✅     |

### 🔒 Security

| Feature                                     | Status |
| ------------------------------------------- | ------ |
| Rate limiting on all sensitive endpoints    | ✅     |
| Profanity filter (form + model level)       | ✅     |
| Content moderation reports                  | ✅     |
| CSRF + XSS protection                       | ✅     |
| File upload validation (type + size)        | ✅     |
| Secure headers (HSTS, CSP, X-Frame-Options) | ✅     |
| Email verification required for login       | ✅     |

### 🌐 Internationalization

| Feature                   | Status |
| ------------------------- | ------ |
| English (en-us)           | ✅     |
| Arabic (ar) — RTL support | ✅     |

### 🎨 UI/UX

| Feature                                     | Status |
| ------------------------------------------- | ------ |
| Dark mode (with OS preference detection)    | ✅     |
| Bootstrap 5 RTL responsive design           | ✅     |
| Open Graph meta tags for social sharing     | ✅     |
| AJAX reactions with WebSocket notifications | ✅     |
| Paginated feeds                             | ✅     |

---

## 🛠️ Tech Stack

<div align="center">

| Layer                | Technology                                   |
| -------------------- | -------------------------------------------- |
| **Backend**          | Django 5.1.7, Python 3.12                    |
| **API**              | Django REST Framework 3.14 + drf-spectacular |
| **Real-time**        | Django Channels 4.0 + WebSockets             |
| **Database**         | PostgreSQL 16 / SQLite 3                     |
| **Cache**            | Redis 7 / DatabaseCache (fallback)           |
| **Async**            | Daphne ASGI server                           |
| **Frontend**         | Bootstrap 5.1, HTML5, CSS3, JavaScript       |
| **Forms**            | django-crispy-forms + crispy-bootstrap5      |
| **Rate Limiting**    | django-ratelimit 4.1                         |
| **Background Tasks** | django-background-tasks                      |
| **Image Processing** | Pillow 10.x                                  |
| **Containerization** | Docker + docker-compose                      |
| **CI/CD**            | GitHub Actions                               |

</div>

---

## 🏗️ Architecture

```
┌──────────────┐      ┌───────────────────┐      ┌──────────────┐
│   Browser /   │◄────►│   Daphne ASGI     │◄────►│   Redis       │
│   Mobile      │      │   (Django +       │      │   (Cache +    │
│               │      │    Channels)      │      │    Channel    │
└──────────────┘      └────────┬──────────┘      │    Layer)     │
                               │                  └──────┬───────┘
                               ▼                         │
┌──────────────────────────────────────────────┐          │
│              Django Application              │          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐  │          │
│  │  posts   │ │  users   │ │notifications │  │          │
│  │  app     │ │  app     │ │    app       │  │          │
│  └──────────┘ └──────────┘ └──────────────┘  │          │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐  │          │
│  │direct_msgs│ │ reports │ │  searchapp   │  │          │
│  └──────────┘ └──────────┘ └──────────────┘  │          │
└──────────────────────┬───────────────────────┘          │
                       │                                  │
                       ▼                                  │
              ┌────────────────┐                          │
              │   PostgreSQL   │◄─────────────────────────┘
              │  /  SQLite     │
              └────────────────┘
```

### App Responsibilities

| App                 | Responsibility                                                |
| ------------------- | ------------------------------------------------------------- |
| **posts**           | CRUD posts, stories, comments, reactions, hashtags, bookmarks |
| **users**           | Auth, profiles, follows, blocks, follow requests, settings    |
| **notifications**   | Real-time + database notifications                            |
| **direct_messages** | WebSocket-powered private chat                                |
| **reports**         | Content moderation and abuse reporting                        |
| **searchapp**       | Cross-model search                                            |

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone and run
git clone https://github.com/neoastra303/socialmedia-app.git
cd socialmedia-app
docker compose up
```

The app will be available at `http://localhost:8000`. Swagger docs at `http://localhost:8000/api/docs/`.

### Option 2: Manual Setup

```bash
git clone https://github.com/neoastra303/socialmedia-app.git
cd socialmedia-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY='your-secret-key'
export DEBUG=True

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

> **Note**: Without Redis, the app falls back to DatabaseCache and InMemoryChannelLayer automatically.

---

## 🔧 Environment Variables

```env
# Required
SECRET_KEY=your-secret-key-here

# Optional (with defaults)
DEBUG=True                                         # Set False for production
REDIS_URL=redis://localhost:6379                   # Falls back to DB cache
DB_NAME=socialmedia_db                             # PostgreSQL (optional)
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=your-email@gmail.com               # For password reset emails
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 📖 API

Interactive Swagger documentation is available at `/api/docs/` when the server is running.

```bash
# OpenAPI schema
GET /api/schema/
```

### Key REST Endpoints

| Method | Endpoint                 | Description       |
| ------ | ------------------------ | ----------------- |
| `GET`  | `/api/posts/`            | List all posts    |
| `GET`  | `/posts/hashtag/<name>/` | Posts by hashtag  |
| `GET`  | `/posts/trending/`       | Trending hashtags |
| `POST` | `/posts/<id>/react/`     | React to a post   |

### WebSocket Endpoints

| Endpoint                               | Description             |
| -------------------------------------- | ----------------------- |
| `ws://host/ws/chat/<conversation_id>/` | Real-time chat          |
| `ws://host/ws/notifications/`          | Real-time notifications |

---

## 🧪 Testing

```bash
# Run all tests (39 test cases)
python manage.py test

# Run specific app tests
python manage.py test posts
python manage.py test users

# Run with verbose output
python manage.py test --verbosity=2

# Check for system issues
python manage.py check
```

### Test Coverage

| Test Suite                 | Tests                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------- |
| `posts/tests.py`           | Model validation, form validation, view integration, profanity filter, bookmarks                        |
| `users/tests.py`           | Profile CRUD, follow/unfollow, block/unblock, privacy, follow requests, settings, password/email change |
| `notifications/tests.py`   | Notification creation                                                                                   |
| `reports/tests.py`         | Report submission                                                                                       |
| `direct_messages/tests.py` | Conversation management                                                                                 |
| **Total**                  | **39 passing**                                                                                          |

---

## 🐳 Docker

```bash
# Build and start
docker compose up --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Run tests
docker compose exec web python manage.py test

# Cleanup expired stories
docker compose exec web python manage.py cleanup_stories
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes with descriptive messages
4. **Run tests** to ensure nothing breaks: `python manage.py test`
5. **Push** to your branch: `git push origin feature/amazing-feature`
6. **Open** a Pull Request

### Commit Guidelines

- Use granular, descriptive commits (one logical change per commit)
- Prefix with the area changed: `feat:`, `fix:`, `test:`, `docs:`, `refactor:`

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <b>Built with ❤️ using Django</b><br/>
  <sub>⭐ Star this repo if you find it useful! ⭐</sub>
</div>

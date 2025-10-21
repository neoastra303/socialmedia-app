# Getting Started

This guide will help you set up the Social Media Platform for development.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git
- Redis server (for caching and background tasks)
- PostgreSQL (recommended for production, SQLite for development)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd socialmedia-app
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 5. Set Up Database

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

## Development Workflow

### Running Tests

```bash
python manage.py test
```

### Code Quality Tools

```bash
# Format code with Black
black .

# Sort imports
isort .

# Lint with Ruff
ruff check . --fix
```

### Adding New Features

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes
3. Add tests
4. Run tests: `python manage.py test`
5. Format code: `black . && isort . && ruff check . --fix`
6. Commit and push: `git add . && git commit -m "message" && git push origin branch-name`
7. Create PR on GitHub
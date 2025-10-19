# Social Media App

A Django-based social media application similar to Instagram/Twitter, featuring posts, reactions, stories, comments, hashtags, search, notifications, and direct messages.

## Features

- User profiles with bio, location, and profile pictures
- Posts with images, hashtags, and reactions (like, love, laugh, angry, sad)
- Stories that expire after 24 hours
- Comments and replies on posts
- Hashtag-based post discovery
- Advanced search for posts and users
- Real-time notifications
- Direct messaging
- Follow/unfollow system
- Rate limiting for security

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd socialmedia-app
   ```

2. Create a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:

   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. Run migrations:

   ```
   python manage.py migrate
   ```

6. Create a superuser:

   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

- Access the admin panel at `/admin/`
- View posts at `/posts/`
- Create posts, add reactions, and interact with features.

## Technologies Used

- Django 5.1
- Django Channels for WebSockets
- Pillow for image processing
- Crispy Forms for form styling
- Bootstrap 5 for UI

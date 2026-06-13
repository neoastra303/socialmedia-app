FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV SECRET_KEY=change-me-in-production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt daphne

COPY . .

RUN mkdir -p /app/logs /app/media /app/staticfiles_build
RUN python manage.py collectstatic --noinput
RUN python manage.py createcachetable --noinput 2>/dev/null || true

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "socialmediaproject.asgi:application"]

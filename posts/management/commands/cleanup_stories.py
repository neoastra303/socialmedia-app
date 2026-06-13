from django.core.management.base import BaseCommand
from django.utils import timezone
from posts.models import Story
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Delete expired stories (older than 24 hours)'

    def handle(self, *args, **options):
        expired = Story.objects.filter(expires_at__lte=timezone.now())
        count = expired.count()
        expired.delete()
        logger.info(f'Deleted {count} expired stories')
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired stories'))

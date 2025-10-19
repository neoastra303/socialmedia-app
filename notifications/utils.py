from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_notification(user, message, notification_type='general', related_user=None, related_post=None):
    # Create notification in database
    notification = Notification.objects.create(
        user=user,
        message=message,
        notification_type=notification_type,
        related_user=related_user,
        related_post=related_post
    )

    # Send real-time notification via WebSocket
    channel_layer = get_channel_layer()
    group_name = f'user_{user.id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'notification': {
                'id': notification.id,
                'message': message,
                'notification_type': notification_type,
                'created_at': notification.created_at.isoformat(),
                'is_read': False
            }
        }
    )

    return notification
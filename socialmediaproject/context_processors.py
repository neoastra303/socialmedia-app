from datetime import datetime

def global_context(request):
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
    else:
        unread_count = 0
    return {
        'current_year': datetime.now().year,
        'unread_notifications_count': unread_count,
    }
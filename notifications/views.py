from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

# Create your views here.

@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def get_unread_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})

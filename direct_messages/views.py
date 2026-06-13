from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Conversation, Message
from .forms import MessageForm
from django.contrib.auth.models import User
from notifications.utils import send_notification

@login_required
def inbox(request):
    conversations = request.user.conversations.prefetch_related('participants').all()
    return render(request, 'messages/inbox.html', {'conversations': conversations})

@login_required
def conversation_detail(request, username):
    other_user = get_object_or_404(User, username=username)
    conversation, created = Conversation.objects.get_or_create_for_users(request.user, other_user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            # Send notification
            send_notification(
                other_user,
                f'رسالة جديدة من {request.user.username}',
                'message',
                related_user=request.user
            )
            return redirect('messages:conversation_detail', username=username)
    else:
        form = MessageForm()

    messages_list = conversation.messages.select_related('sender').all()
    return render(request, 'messages/conversation.html', {
        'conversation': conversation,
        'messages': messages_list,
        'other_user': other_user,
        'form': form
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        content = request.POST.get('content')

        recipient = get_object_or_404(User, username=recipient_username)
        conversation, created = Conversation.objects.get_or_create_for_users(request.user, recipient)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        # Send notification
        send_notification(
            recipient,
            f'رسالة جديدة من {request.user.username}',
            'message',
            related_user=request.user
        )

        return JsonResponse({'status': 'success', 'message_id': message.id})

    return JsonResponse({'status': 'error'}, status=400)

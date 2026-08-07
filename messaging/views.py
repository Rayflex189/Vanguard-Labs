from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from .models import Conversation, Participant, Message, MessageReadReceipt
from .forms import ConversationCreateForm, MessageForm

@login_required
def conversation_list(request):
    """Display list of conversations for the current user."""
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    # Annotate unread count
    for conv in conversations:
        conv.unread_count = conv.get_unread_count_for_user(request.user)
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, pk):
    """Display a single conversation with messages."""
    conversation = get_object_or_404(Conversation, participants=request.user, pk=pk)
    if request.user not in conversation.participants.all():
        raise PermissionDenied
    # Mark all messages as read
    conversation.mark_as_read_for_user(request.user)
    messages_list = conversation.message_set.filter(is_deleted=False).select_related('sender')
    # Prepare form
    form = MessageForm()
    # Get participant info
    participant = conversation.get_participant_for_user(request.user)
    context = {
        'conversation': conversation,
        'messages': messages_list,
        'form': form,
        'participant': participant,
        'is_group': conversation.is_group,
    }
    return render(request, 'messaging/conversation_detail.html', context)

@login_required
def send_message(request, pk):
    """Send a new message in a conversation."""
    conversation = get_object_or_404(Conversation, participants=request.user, pk=pk)
    if request.user not in conversation.participants.all():
        raise PermissionDenied
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            # Update conversation last_message and updated_at
            conversation.last_message = message
            conversation.updated_at = timezone.now()
            conversation.save(update_fields=['last_message', 'updated_at'])
            # Mark this message as read by sender
            MessageReadReceipt.objects.create(message=message, user=request.user, read_at=timezone.now())
            # Redirect back to detail
            return redirect('messaging:detail', pk=conversation.pk)
    return redirect('messaging:detail', pk=conversation.pk)

@login_required
def mark_conversation_read(request, pk):
    """Mark all messages in a conversation as read."""
    conversation = get_object_or_404(Conversation, participants=request.user, pk=pk)
    conversation.mark_as_read_for_user(request.user)
    return JsonResponse({'status': 'ok'})

@login_required
def unread_count(request):
    """Return total unread messages count for the current user."""
    total = 0
    for conv in Conversation.objects.filter(participants=request.user):
        total += conv.get_unread_count_for_user(request.user)
    return JsonResponse({'unread_count': total})

@login_required
def create_conversation(request):
    """Start a new conversation (direct or group)."""
    if request.method == 'POST':
        form = ConversationCreateForm(request.POST, user=request.user)
        if form.is_valid():
            participants = form.cleaned_data['participants']
            is_group = form.cleaned_data.get('is_group', False)
            subject = form.cleaned_data.get('subject', '')
            # Create conversation
            conversation = Conversation.objects.create(subject=subject, is_group=is_group)
            # Add participants (including sender)
            users = list(participants) + [request.user]
            for user in users:
                Participant.objects.create(conversation=conversation, user=user, is_admin=(user == request.user))
            return redirect('messaging:detail', pk=conversation.pk)
    else:
        form = ConversationCreateForm(user=request.user)
    return render(request, 'messaging/conversation_form.html', {'form': form})

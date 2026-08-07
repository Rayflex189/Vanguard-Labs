from .models import Conversation

def unread_messages_count(request):
    if request.user.is_authenticated:
        total = 0
        for conv in Conversation.objects.filter(participants=request.user):
            total += conv.get_unread_count_for_user(request.user)
        return {'unread_messages_count': total}
    return {'unread_messages_count': 0}

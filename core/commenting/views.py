from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import permission_required
from core.decorators import owner_or_perm_required
from django.contrib.comments.models import Comment
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
import django.contrib.comments.views.moderation as moderation
        
@owner_or_perm_required(Comment, 'comments.can_change')
def delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment_object = comment.content_object
    c = str(comment)
    comment.delete()
    request.user.message_set.create(message=_(u'Comment deleted')+': '+c)
    return HttpResponseRedirect(comment_object.get_absolute_url())

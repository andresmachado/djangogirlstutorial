from django.core.exceptions import PermissionDenied

def can_view_post(request, post):
    if request.user.is_authenticated and post.author.id == request.user.id:
        request.can_edit = True
        return request

def can_edit_post(request, post):
    if request.user.is_authenticated and post.author.id == request.user.id:
        request.can_edit = True
        return request
    raise PermissionDenied
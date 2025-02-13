from django.contrib.auth.decorators import login_required
from functools import wraps
from django.core.exceptions import PermissionDenied


def group_required(group_name):
    """
    Decorator to restrict view access to users in a specific group.
    """
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name=group_name).exists():
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

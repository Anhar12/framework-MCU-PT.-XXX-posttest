from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps

def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role == group_names[0] or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied

        return _wrapped_view
    return decorator
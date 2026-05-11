from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """Restrict a view to users with one of the given roles."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in roles:
                messages.error(request, 'You do not have permission to access that page.')
                return redirect(request.user.get_dashboard_url())
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def client_required(view_func):
    return role_required('CLIENT')(view_func)


def advocate_required(view_func):
    return role_required('ADVOCATE')(view_func)


def admin_required(view_func):
    return role_required('ADMIN')(view_func)

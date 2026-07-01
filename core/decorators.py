from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from accounts.permissions import user_can_view_finance


def admin_required(view_func):
    """Доступ к финансам и отчётам — только директор."""

    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not user_can_view_finance(request.user):
            messages.error(request, 'Раздел доступен только директору.')
            return redirect('core:home')
        return view_func(request, *args, **kwargs)

    return wrapper

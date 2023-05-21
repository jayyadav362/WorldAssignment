from django.shortcuts import *
from functools import wraps


def is_logged_in(func=None, redirect_url=None):
    def decorator(function):
        @wraps(function)
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return function(request, *args, **kwargs)
        return wrap

    if func is None:
        return decorator
    else:
        return decorator(func)
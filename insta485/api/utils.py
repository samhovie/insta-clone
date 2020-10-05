"""Insta485 API utility functions."""
from functools import wraps

import flask
from insta485.views.utils import get_current_user

def requires_login(route):
    """Change route so it raises a 403 if no user is authenticated."""
    @wraps(route)
    def with_login_required(*args, **kwargs):
        if get_current_user() is None:
            flask.abort(403)
        return route(*args, **kwargs)

    return with_login_required

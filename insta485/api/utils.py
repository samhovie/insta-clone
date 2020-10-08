"""Insta485 API utility functions."""
from functools import wraps

import flask
from insta485.views.utils import get_current_user, remove_comment, add_comment


def api_error(code):
    """Abort with a REST API-compatible error and status code <code>."""
    messages = {
        403: "Unauthorized",
        404: "Not Found",
    }
    response = flask.jsonify(message=messages[code], status_code=code)
    response.status_code = code
    flask.abort(response)


def requires_login(route):
    """Change route so it raises a 403 if no user is authenticated."""
    @wraps(route)
    def with_login_required(*args, **kwargs):
        if get_current_user() is None:
            api_error(403)
        return route(*args, **kwargs)

    return with_login_required

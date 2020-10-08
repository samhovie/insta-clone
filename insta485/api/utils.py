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


def like_post(username, post_id):
    """Create entry for username liking post_id in likes."""
    connection = insta485.model.get_db()

    like = connection.execute(
        "SELECT * FROM likes "
        "WHERE owner = ? AND postid = ?;",
        (username, post_id)
    ).fetchone()

    if like is not None:
        return

    connection.execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES (?, ?);",
        (username, post_id)
    )


def unlike_post(username, post_id):
    """Remove entry for username liking post_id in likes."""
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM likes "
        "WHERE owner = ? AND postid = ?;",
        (username, post_id)
    )


def requires_login(route):
    """Change route so it raises a 403 if no user is authenticated."""
    @wraps(route)
    def with_login_required(*args, **kwargs):
        if get_current_user() is None:
            api_error(403)
        return route(*args, **kwargs)

    return with_login_required

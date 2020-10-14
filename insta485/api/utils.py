"""Insta485 API utility functions."""
from functools import wraps

import flask
import insta485
from insta485.views.utils import get_current_user


add_comment = insta485.views.utils.add_comment
remove_comment = insta485.views.utils.remove_comment


def api_error(code, additional_data=None):
    """Abort with a REST API-compatible error and status code <code>."""
    messages = {
        403: "Unauthorized",
        404: "Not Found",
        409: "Conflict",
    }
    if additional_data is None:
        additional_data = {}
    response = flask.jsonify(
        message=messages[code],
        status_code=code,
        **additional_data
    )
    response.status_code = code
    flask.abort(response)


def like_post(username, post_id):
    """Create entry for username liking post_id in likes."""
    cursor = insta485.model.get_db()

    cursor.execute(
        " SELECT * FROM likes "
        " WHERE owner = %s AND postid = %s;",
        (username, post_id)
    )
    like = cursor.fetchone()

    if like is not None:
        return False

    cursor.execute(
        " INSERT INTO likes (owner, postid) "
        " VALUES (%s, %s);",
        (username, post_id)
    )
    return True


def unlike_post(username, post_id):
    """Remove entry for username liking post_id in likes."""
    cursor = insta485.model.get_db()
    cursor.execute(
        " DELETE FROM likes "
        " WHERE owner = %s AND postid = %s;",
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


def confirm_post_exists(post_id):
    """Confirm that a post with ID <post_id> exists."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "SELECT postid FROM posts WHERE postid = %s ",
        (post_id,)
    )
    post_exists = cursor.fetchone() is not None
    if not post_exists:
        api_error(404)

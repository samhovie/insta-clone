"""REST API for likes."""
import flask
import insta485
from insta485.api.utils import (
    api_error,
    confirm_post_exists,
    get_current_user,
    like_post,
    requires_login,
    unlike_post,
)


@insta485.app.route('/api/v1/p/<int:post_id>/likes/', methods=['GET'])
@requires_login
def get_likes(post_id):
    """Return likes on the post with ID <post_id>.

    Example:
    {
      "logname_likes_this": 1,
      "likes_count": 3,
      "postid": 1,
      "url": "/api/v1/p/1/likes/"
    }
    """
    connection = insta485.model.get_db()
    current_user = get_current_user()

    confirm_post_exists(post_id)

    num_likes = connection.execute(
        "SELECT COUNT(*) FROM likes "
        "WHERE postid = ? ",
        (post_id,)
    ).fetchone()["COUNT(*)"]

    logname_likes_this = connection.execute(
        "SELECT * FROM likes "
        "WHERE owner = ? AND postid = ?;",
        (current_user["username"], post_id)
    ).fetchone() is not None

    context = {
        "logname_likes_this": int(logname_likes_this),
        "likes_count": num_likes,
        "postid": post_id,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/p/<int:post_id>/likes/', methods=['POST'])
@requires_login
def add_like(post_id):
    """Add a like to the post with ID <post_id>."""
    confirm_post_exists(post_id)

    current_user = get_current_user()

    result = {
        "logname": current_user["username"],
        "postid": post_id,
    }

    if not like_post(current_user["username"], post_id):
        api_error(409, result)
    return flask.jsonify(**result), 201


@insta485.app.route('/api/v1/p/<int:post_id>/likes/', methods=['DELETE'])
@requires_login
def remove_like(post_id):
    """Remove a like from the post with ID <post_id>."""
    confirm_post_exists(post_id)
    unlike_post(get_current_user()["username"], post_id)
    return flask.jsonify({}), 204

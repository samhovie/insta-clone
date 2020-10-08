"""REST API for likes."""
import flask
import insta485
from insta485.api.utils import requires_login


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=['GET'])
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
    context = {
        "logname_likes_this": 1,
        "likes_count": 3,
        "postid": post_id,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/p/<int:post_id>/likes/', methods=['POST'])
@requires_login
def add_like(post_id):
    """Add a like to the post with ID <post_id>."""
    return "Hello from post with ID " + post_id


@insta485.app.route('/api/v1/p/<int:post_id>/likes/', methods=['DELETE'])
@requires_login
def remove_like(post_id):
    """Remove a like from the post with ID <post_id>."""
    return "Hello from post with ID " + post_id

"""REST API for likes."""
import flask
import insta485


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["GET"])
def get_likes(postid_url_slug):
    """Return likes on postid.

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
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return flask.jsonify(**context)

"""REST API for comments."""
import flask
import insta485
from insta485.api.utils import (
    confirm_post_exists,
    api_error,
    requires_login,
    get_current_user,
)


@insta485.app.route('/api/v1/p/<int:post_id>/comments/', methods=['GET'])
@requires_login
def get_comments(post_id):
    """Return comments for the post with ID <post_id>.

    Example:
    {
      "comments": [
        {
          "commentid": 1,
          "owner": "awdeorio",
          "owner_show_url": "/u/awdeorio/",
          "postid": 3,
          "text": "#chickensofinstagram"
        },
        {
          "commentid": 2,
          "owner": "jflinn",
          "owner_show_url": "/u/jflinn/",
          "postid": 3,
          "text": "I <3 chickens"
        },
        {
          "commentid": 3,
          "owner": "michjc",
          "owner_show_url": "/u/michjc/",
          "postid": 3,
          "text": "Cute overload!"
        }
      ],
      "url": "/api/v1/p/3/comments/"
    }
    """

    confirm_post_exists(post_id)

    cursor = insta485.model.get_db()
    cursor.execute(
        "SELECT commentid, owner, text FROM comments "
        "WHERE postid = %s "
        "ORDER BY commentid ASC ",
        (post_id,)
    )
    comments_sql = cursor.fetchall()

    comments = list(map(lambda comment_sql: {
        "commentid": int(comment_sql["commentid"]),
        "owner": comment_sql["owner"],
        "owner_show_url": flask.url_for(
            "show_profile",
            user_id=comment_sql["owner"]
        ),
        "postid": post_id,
        "text": comment_sql["text"],
    }, comments_sql))

    return flask.jsonify(comments=comments, url=flask.request.path)


@insta485.app.route('/api/v1/p/<int:post_id>/comments/', methods=['POST'])
@requires_login
def add_comment(post_id):
    """Add a comment to the post with ID <post_id>."""
    cursor = insta485.model.get_db()

    confirm_post_exists(post_id)

    if flask.request.json is None or "text" not in flask.request.json:
        api_error(400)

    current_user = get_current_user()
    comment_id = insta485.api.utils.add_comment(
        current_user["username"],
        post_id,
        flask.request.json["text"]
    )

    comment = {
        "commentid": int(comment_id),
        "owner": current_user["username"],
        "owner_show_url": flask.url_for(
            "show_profile",
            user_id=current_user["username"]
        ),
        "postid": post_id,
        "text": flask.request.json["text"],
    }

    return flask.jsonify(**comment), 201

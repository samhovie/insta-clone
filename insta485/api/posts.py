"""REST API for getting information about posts."""
import flask
import insta485
from insta485.api.utils import requires_login, get_current_user


@insta485.app.route('/api/v1/p/', methods=['GET'])
@requires_login
def get_posts():
    """Return the <size> newest posts, offset by <page> pages.

    Example:
    {
      "next": "",
      "results": [
        {
          "postid": 3,
          "url": "/api/v1/p/3/"
        },
        {
          "postid": 2,
          "url": "/api/v1/p/2/"
        },
        {
          "postid": 1,
          "url": "/api/v1/p/1/"
        }
      ],
      "url": "/api/v1/p/"
    }
    """
    current_user = get_current_user()

    size = flask.request.args.get("size", default=10, type=int)
    size = size if size >= 0 else 0

    page = flask.request.args.get("page", default=0, type=int)
    page = page if page >= 0 else 0

    limit = size
    offset = page * size

    connection = insta485.model.get_db()
    posts_sql = connection.execute(
        "SELECT posts.postid FROM posts "
        "INNER JOIN users on users.username = posts.owner "
        "WHERE posts.owner = ? "
        "OR posts.owner IN "
        "    (SELECT username2 FROM following WHERE username1 = ?) "
        "ORDER BY posts.postid DESC "
        "LIMIT ? offset ? ",
        (current_user["username"], current_user["username"], limit, offset)
    ).fetchall()

    posts = list(map(lambda post_sql: {
        "postid": int(post_sql["postid"]),
        "url": flask.url_for("get_post", postid=int(post_sql["postid"])),
    }, posts_sql))

    return flask.jsonify(posts)


@insta485.app.route('/api/v1/p/<int:postid>', methods=['GET'])
@requires_login
def get_post(postid):
    """Return information about the post with ID <postid>."""
    return f"TODO: Post with id {postid} here"

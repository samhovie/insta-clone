"""REST API for getting information about posts."""
import flask
import insta485
from insta485.api.utils import api_error, requires_login, get_current_user


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
    page = flask.request.args.get("page", default=0, type=int)

    if size < 0 or page < 0:
        api_error(400)

    limit = size + 1
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
    more_posts = (len(posts_sql) == limit)
    if more_posts:
        posts_sql.pop()

    posts = list(map(lambda post_sql: {
        "postid": int(post_sql["postid"]),
        "url": flask.url_for("get_post", post_id=int(post_sql["postid"])),
    }, posts_sql))

    next_url = ""
    if more_posts:
        next_url = flask.url_for("get_posts", size=size, page=page + 1)

    return flask.jsonify(next=next_url, results=posts, url=flask.request.path)


@insta485.app.route('/api/v1/p/<int:post_id>/', methods=['GET'])
@requires_login
def get_post(post_id):
    """Return information about the post with ID <post_id>.

    Example:
    {
      "age": "2017-09-28 04:33:28",
      "img_url": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
      "owner": "awdeorio",
      "owner_img_url": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "owner_show_url": "/u/awdeorio/",
      "post_show_url": "/p/3/",
      "url": "/api/v1/p/3/"
    }
    """
    connection = insta485.model.get_db()
    post_sql = connection.execute(
        "SELECT posts.*, users.filename AS owner_filename FROM posts "
        "INNER JOIN users on users.username = posts.owner "
        "WHERE posts.postid = ? ",
        (post_id,)
    ).fetchone()

    if post_sql is None:
        api_error(404)

    post = {
        "age": post_sql["created"],
        "img_url": flask.url_for(
            "show_upload",
            path=post_sql["filename"]
        ),
        "owner": post_sql["owner"],
        "owner_img_url": flask.url_for(
            "show_upload",
            path=post_sql["owner_filename"]
        ),
        "owner_show_url": flask.url_for(
            "show_profile",
            user_id=post_sql["owner"]
        ),
        "post_show_url": flask.url_for(
            "show_post",
            post_id=post_id
        ),
        "url": flask.url_for("get_post", post_id=post_id),
    }
    return flask.jsonify(**post)

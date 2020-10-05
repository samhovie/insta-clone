"""
Insta485 index (main) view.

URLs include:
/
"""
import arrow
import flask
import insta485

from insta485.views.utils import (
    get_current_user,
    like_unlike_or_comment,
    requires_login,
)


@insta485.app.route('/', methods=['GET', 'POST'])
@requires_login
def show_index():
    """Display / route."""
    # Connect to database
    connection = insta485.model.get_db()
    current_user = get_current_user()

    # Handle POST requests for submitting likes, unlikes and comments
    if flask.request.method == "POST":
        like_unlike_or_comment(current_user)

    # Retreive data to render home page template

    # Each post will contain postid, filename, owner, created, poster_filename
    # for all posts by current_user or from who they're following
    posts = connection.execute(
        "SELECT posts.*, users.filename as poster_filename "
        "FROM posts "
        "INNER JOIN users ON users.username = posts.owner "
        "WHERE posts.owner = ? "
        "OR posts.owner IN "
        "   (SELECT username2 FROM following WHERE username1 = ?) "
        "ORDER BY posts.created, posts.postid ASC;",
        (current_user["username"], current_user["username"])
    ).fetchall()
    # Humanize timestamps
    for post in posts:
        post["created"] = arrow.get(post["created"]).humanize()

    likes = connection.execute(
        "SELECT postid, owner FROM likes "
        "WHERE postid IN "
        "   (SELECT postid FROM posts WHERE owner = ? "
        "   OR owner in "
        "       (SELECT username2 FROM following WHERE username1 = ?));",
        (current_user["username"], current_user["username"])
    )
    # Put likes.owner for each post into separate list
    # Access in template using postid, length of list = num likes
    likes_by_post = {}
    for post in posts:
        likes_by_post[post["postid"]] = []
    for like in likes:
        likes_by_post[like["postid"]].append(like["owner"])

    comments = connection.execute(
        "SELECT commentid, postid, text, owner FROM comments "
        "WHERE postid IN "
        "   (SELECT postid FROM posts WHERE owner = ? "
        "   OR owner IN "
        "       (SELECT username2 FROM following WHERE username1 = ?)) "
        "ORDER BY created, commentid ASC; ",
        (current_user["username"], current_user["username"])
    ).fetchall()
    # Put comments for each post into separate list
    # Access in template using postid
    comments_by_post = {}
    for post in posts:
        comments_by_post[post["postid"]] = []
    for comment in comments:
        comments_by_post[comment["postid"]].append(comment)

    # Render home page template
    context = {
        'current_user': current_user,
        'posts': posts,
        'all_likes': likes_by_post,
        'all_comments': comments_by_post,
        'single_post_view': False,
    }
    return flask.render_template("index.html", **context)

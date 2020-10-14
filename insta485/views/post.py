"""
Insta485 post views.

URLs include:
/p/<post id>/
"""
import arrow
import flask
import insta485

from insta485.views.utils import (
    like_unlike_or_comment,
    requires_login,
    get_current_user,
    remove_comment,
    remove_post,
)


@insta485.app.route('/p/<post_id>/', methods=['GET', 'POST'])
@requires_login
def show_post(post_id):
    """Display /p/<post id>/ route."""
    # Connect to database
    cursor = insta485.model.get_db()
    current_user = get_current_user()

    # Handle POST requests for submitting likes, unlikes and comments, and
    # for deleting posts and comments
    if flask.request.method == "POST":
        if "delete" in flask.request.form:
            remove_post(current_user["username"], flask.request.form["postid"])
            return flask.redirect(
                flask.url_for('show_profile', user_id=current_user["username"])
            )

        if "uncomment" in flask.request.form:
            remove_comment(current_user["username"],
                           flask.request.form["commentid"])
        else:
            like_unlike_or_comment(current_user)

    # Post will contain postid, filename, owner, created, poster_filename
    cursor.execute(
        "SELECT posts.*, users.filename as poster_filename FROM posts "
        "INNER JOIN users on users.username = posts.owner "
        "WHERE postid = %s;",
        (post_id)
    )
    post = cursor.fetchone()
    if post is None:
        flask.abort(404)
    # Humanize timestamp
    post["created"] = arrow.get(post["created"]).humanize()

    # Retrieve likes for post
    cursor.execute(
        "SELECT owner FROM likes "
        "WHERE postid = %s;",
        (post_id)
    )
    likes = cursor.fetchall()
    # Convert likes to list of owners
    like_owners = []
    for like in likes:
        like_owners.append(like["owner"])

    # Retrieve comments for post
    cursor.execute(
        "SELECT commentid, owner, text FROM comments "
        "WHERE postid = %s "
        "ORDER BY created, commentid ASC;",
        (post_id)
    )
    comments = cursor.fetchall()

    context = {
        'current_user': current_user,
        'post': post,
        'likes': like_owners,
        'comments': comments,
        'single_post_view': True,
    }
    return flask.render_template('post.html', **context)

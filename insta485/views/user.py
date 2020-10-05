"""
Insta485 user views.

URLs include:
/u/<user id>/
/u/<user id>/followers/
/u/<user id>/following/
"""
# import flask
import flask
import insta485
from insta485.views.utils import (
    requires_login,
    get_current_user,
    add_follower,
    remove_follower,
    save_upload,
    create_post,
)


@insta485.app.route('/u/<user_id>/', methods=['GET', 'POST'])
@requires_login
def show_profile(user_id):
    """Display /u/<user_id>/ route."""
    # Connect to db
    connection = insta485.model.get_db()
    current_user = get_current_user()

    # Handle POST requests
    if flask.request.method == "POST":
        if "follow" in flask.request.form:
            add_follower(current_user["username"],
                         flask.request.form["username"])
        elif "unfollow" in flask.request.form:
            remove_follower(current_user["username"],
                            flask.request.form["username"])
        elif "create_post" in flask.request.form:
            filename = save_upload(flask.request.files["file"])
            create_post(current_user["username"], filename)

    # Retrieve user data if user exists
    profile_user = connection.execute(
        "SELECT username, fullname, email, filename FROM users "
        "WHERE username = ?;",
        (user_id,)
    ).fetchone()
    if profile_user is None:
        flask.abort(404)

    # Retrieve follower and following count
    num_followers = connection.execute(
        "SELECT COUNT(*) as count FROM following "
        "WHERE username2 = ?;",
        (user_id,)
    ).fetchone()
    num_following = connection.execute(
        "SELECT COUNT(*) as count FROM following "
        "WHERE username1 = ?;",
        (user_id,)
    ).fetchone()

    # Check if current user follows profile user
    relationship = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 = ? "
        "AND username2 = ?;",
        (current_user["username"], user_id)
    ).fetchone()
    current_user_is_following = relationship is not None

    # Retrieve posts for user
    posts = connection.execute(
        "SELECT postid, filename FROM posts "
        "WHERE owner = ? "
        "ORDER BY created, postid;",
        (user_id,)
    ).fetchall()

    context = {
        "profile_user": profile_user,
        "current_user": current_user,
        "follower_count": num_followers["count"],
        "following_count": num_following["count"],
        "current_user_is_following": current_user_is_following,
        "posts": posts,
    }
    return flask.render_template('profile.html', **context)


@insta485.app.route('/u/<user_id>/followers/', methods=['GET', 'POST'])
@requires_login
def show_followers(user_id):
    """Display /u/<user_id>/followers/ route."""
    connection = insta485.model.get_db()
    current_user = get_current_user()

    if flask.request.method == 'POST':
        if flask.request.form.get('follow') is not None:
            add_follower(
                current_user['username'],
                flask.request.form['username']
            )

        elif flask.request.form.get('unfollow') is not None:
            remove_follower(
                current_user['username'],
                flask.request.form['username']
            )

    # followers following me
    followers = connection.execute(
        "SELECT users.username, users.filename "
        "FROM users INNER JOIN following ON "
        " users.username = following.username1 "
        "WHERE following.username2 = ? ",
        (user_id,)
    ).fetchall()

    # who I follow
    following = connection.execute(
        "SELECT users.username, users.filename FROM users "
        " INNER JOIN following ON users.username = following.username2 "
        "WHERE following.username1 = ?",
        (current_user['username'],)
    ).fetchall()
    following = list(map(lambda user: user['username'], following))

    # check if I follow each person that follows me
    for follower in followers:
        if follower['username'] == current_user['username']:
            follower['relate'] = ""
        else:
            if follower['username'] in following:
                follower['relate'] = "following"
            else:
                follower['relate'] = "not following"

    context = {
            'logname': current_user['username'],
            'current_user': current_user,
            'followers': followers,
    }

    return flask.render_template("followers.html", **context)


@insta485.app.route('/u/<user_id>/following/', methods=['GET', 'POST'])
@requires_login
def show_following(user_id):
    """Display /u/<user_id>/following/ route."""
    connection = insta485.model.get_db()
    current_user = get_current_user()

    if flask.request.method == 'POST':
        if flask.request.form.get('follow') is not None:
            add_follower(
                current_user['username'],
                flask.request.form['username']
            )

        elif flask.request.form.get('unfollow') is not None:
            remove_follower(
                current_user['username'],
                flask.request.form['username']
            )

    # followers following me
    profile_following = connection.execute(
        "SELECT users.username, users.filename FROM users "
        " INNER JOIN following ON users.username = following.username2 "
        "WHERE following.username1 = ? ",
        (user_id,)
    ).fetchall()

    # who I follow
    current_u_following = connection.execute(
        "SELECT users.username, users.filename "
        "FROM users INNER JOIN following ON "
        "users.username = following.username2 "
        "WHERE following.username1 = ?",
        (current_user['username'],)
    ).fetchall()
    current_u_following = list(map(
        lambda user: user['username'], current_u_following
    ))

    # check if I follow each person that follows me
    for follower in profile_following:
        if follower['username'] == current_user['username']:
            follower['relate'] = ""
        else:
            if follower['username'] in current_u_following:
                follower['relate'] = "following"
            else:
                follower['relate'] = "not following"

    context = {
            'logname': current_user['username'],
            'current_user': current_user,
            'following': profile_following,
    }

    return flask.render_template("following.html", **context)

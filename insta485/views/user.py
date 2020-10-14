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
    cursor = insta485.model.get_db()
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
    cursor.execute(
        "SELECT username, fullname, email, filename FROM users "
        "WHERE username = %s;",
        (user_id,)
    )
    profile_user = cursor.fetchone()
    if profile_user is None:
        flask.abort(404)

    # Retrieve follower and following count
    cursor.execute(
        "SELECT COUNT(*) as count FROM following "
        "WHERE username2 = %s;",
        (user_id,)
    )
    num_followers = cursor.fetchone()
    cursor.execute(
        "SELECT COUNT(*) as count FROM following "
        "WHERE username1 = %s;",
        (user_id,)
    )
    num_following = cursor.fetchone()

    # Check if current user follows profile user
    cursor.execute(
        "SELECT * FROM following "
        "WHERE username1 = %s "
        "AND username2 = %s;",
        (current_user["username"], user_id)
    )
    relationship = cursor.fetchone()
    current_user_is_following = relationship is not None

    # Retrieve posts for user
    cursor.execute(
        "SELECT postid, filename FROM posts "
        "WHERE owner = %s "
        "ORDER BY created, postid;",
        (user_id,)
    )
    posts = cursor.fetchall()

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
    cursor = insta485.model.get_db()
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
    cursor.execute(
        "SELECT users.username, users.filename "
        "FROM users INNER JOIN following ON "
        " users.username = following.username1 "
        "WHERE following.username2 = %s ",
        (user_id,)
    )
    followers = cursor.fetchall()

    # who I follow
    cursor.execute(
        "SELECT users.username, users.filename FROM users "
        " INNER JOIN following ON users.username = following.username2 "
        "WHERE following.username1 = %s",
        (current_user['username'],)
    )
    following = cursor.fetchall()
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
    cursor = insta485.model.get_db()
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
    cursor.execute(
        "SELECT users.username, users.filename FROM users "
        " INNER JOIN following ON users.username = following.username2 "
        "WHERE following.username1 = %s ",
        (user_id,)
    )
    profile_following = cursor.fetchall()

    # who I follow
    cursor.execute(
        "SELECT users.username, users.filename "
        "FROM users INNER JOIN following ON "
        "users.username = following.username2 "
        "WHERE following.username1 = %s",
        (current_user['username'],)
    )
    current_u_following = cursor.fetchall()
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

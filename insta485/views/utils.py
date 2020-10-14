"""Insta485 view utility functions."""
from functools import wraps
import hashlib
import pathlib
import uuid

import flask
import insta485

# TODO TEMP:
import sys

def save_upload(fileobj):
    """Save the file to the uploads directory. Returns the filename."""
    suffix = pathlib.Path(fileobj.filename).suffix
    uuid_basename = f"{uuid.uuid4().hex}{suffix}"
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


def delete_upload(filename):
    """Delete a file from the uploads directory."""
    path = insta485.app.config["UPLOAD_FOLDER"]/filename
    path.unlink()


def create_hash(password):
    """Create a salted hash for password that can be stored in the database."""
    algorithm = "sha512"
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode("utf-8"))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


def verify_credentials(username, password):
    """Return whether a user with the given username and password exists."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "SELECT password FROM users WHERE username = %s",
        (username,)
    )
    users = cursor.fetchall()

    # No users were found with the username.
    if len(users) != 1:
        return False

    [algorithm, salt, password_hash] = users[0]["password"].split("$")
    hash_obj = hashlib.new(algorithm)
    hash_obj.update((salt + password).encode("utf-8"))
    return hash_obj.hexdigest() == password_hash


def create_user(username, fullname, email, password, image_file):
    """Create a user with the given information."""
    cursor = insta485.model.get_db()

    # If a user with this username already exists, raise a conflict error.
    cursor.execute(
        "SELECT username FROM users WHERE username = %s",
        (username,)
    )
    if len(cursor.fetchall()) != 0:
        flask.abort(409)

    # If no password is provided, raise a bad request error.
    if password == "":
        flask.abort(400)

    filename = save_upload(image_file)

    cursor.execute(
        "INSERT INTO users(username, fullname, email, filename, password)"
        "VALUES (:username, :fullname, :email, :filename, :password)",
        {
          "username": username,
          "fullname": fullname,
          "email": email,
          "filename": filename,
          "password": create_hash(password),
        }
    )


def update_user(username, fullname, email, old_file_name, image_file):
    """Update the user with username to have the given information."""
    cursor = insta485.model.get_db()

    if image_file is not None:
        delete_upload(old_file_name)
        filename = save_upload(image_file)
        cursor.execute(
            "UPDATE users "
            "SET fullname = :fullname, email = :email, filename = :filename "
            "WHERE username = :username",
            {
                "username": username,
                "fullname": fullname,
                "email": email,
                "filename": filename,
            }
        )
    else:
        cursor.execute(
            "UPDATE users "
            "SET fullname = :fullname, email = :email "
            "WHERE username = :username",
            {
                "username": username,
                "fullname": fullname,
                "email": email,
            }
        )


def get_current_user():
    """
    Return a dictionary containing information about the logged-in user.

    If no user is authenticated, returns None.
    """
    if "username" not in flask.session or "user_created" not in flask.session:
        return None
    cursor = insta485.model.get_db()
    cursor.execute(
        "SELECT username, fullname, email, filename FROM users "
        "WHERE username = %s AND created = %s",
        (flask.session["username"], flask.session["user_created"])
    )
    users = cursor.fetchall()
    if len(users) != 1:
        del flask.session["username"]
        del flask.session["user_created"]
        return None
    return users[0]


def login(username):
    """Set cookies such that the current user is logged in as `username`."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "SELECT created FROM users WHERE username = %s",
        (username,)
    )
    users = cursor.fetchall()
    if len(users) != 1:
        flask.abort(500)
    flask.session["username"] = username
    flask.session["user_created"] = str(users[0]["created"])


def logout():
    """Log out the current user. Requires that one is logged in."""
    del flask.session["username"]
    del flask.session["user_created"]


def requires_login(route):
    """Change route so it redirects to login if no user is authenticated."""
    @wraps(route)
    def with_login_required(*args, **kwargs):
        if get_current_user() is None:
            return flask.redirect(flask.url_for("show_login"))
        return route(*args, **kwargs)

    return with_login_required


def create_post(username, filename):
    """Create post entry for username."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "INSERT INTO posts (owner, filename) "
        "VALUES (%s, %s);",
        (username, filename)
    )


def remove_post(username, post_id):
    """Remove post_id if username is post owner."""
    cursor = insta485.model.get_db()

    # Check if post exists and is owned by username, and also get post filename
    cursor.execute(
        "SELECT owner, filename FROM posts "
        "WHERE postid = %s;",
        (post_id)
    )
    post_info = cursor.fetchone()
    if post_info is None:
        flask.abort(404)
    elif username != post_info["owner"]:
        flask.abort(403)

    # Post exists and username owns it so delete all information for it
    cursor.execute(
        "DELETE FROM posts "
        "WHERE postid = %s;",
        (post_id)
    )
    delete_upload(post_info["filename"])


def like_post(username, post_id):
    """Create entry for username liking post_id in likes."""
    cursor = insta485.model.get_db()

    cursor.execute(
        "SELECT * FROM likes "
        "WHERE owner = %s AND postid = %s;",
        (username, post_id)
    )
    like = cursor.fetchone()

    if like is not None:
        flask.abort(400)

    cursor.execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES (%s, %s);",
        (username, post_id)
    )


def unlike_post(username, post_id):
    """Remove entry for username liking post_id in likes."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "DELETE FROM likes "
        "WHERE owner = %s AND postid = %s;",
        (username, post_id)
    )


def add_comment(username, post_id, text):
    """Add comment by username on post_id."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "INSERT INTO comments (owner, postid, text) "
        "VALUES (%s, %s, %s) RETURNING commentid;",
        (username, post_id, text)
    )
    return cursor.fetchone()["commentid"]


def remove_comment(username, comment_id):
    """Remove comment_id if username is comment owner."""
    cursor = insta485.model.get_db()

    # Check if comment exists and username is comment owner
    cursor.execute(
        "SELECT owner FROM comments "
        "WHERE commentid = %s;",
        (comment_id)
    )
    comment_owner = cursor.fetchone()
    if comment_owner is None:
        flask.abort(404)
    elif username != comment_owner["owner"]:
        flask.abort(403)

    # Comment exists and username owns it so delete it
    cursor.execute(
        "DELETE FROM comments "
        "WHERE commentid = %s;",
        (comment_id)
    )


def add_follower(username1, username2):
    """Add username1 as follower of username2."""
    cursor = insta485.model.get_db()

    cursor.execute(
        "SELECT * FROM following "
        "WHERE username1 = %s "
        "AND username2 = %s;",
        (username1, username2)
    )
    already_following = cursor.fetchone() is not None

    if already_following:
        flask.abort(400)

    cursor.execute(
        "INSERT INTO following (username1, username2) "
        "VALUES (%s, %s);",
        (username1, username2)
    )


def remove_follower(username1, username2):
    """Remove username1 from followers of username2."""
    cursor = insta485.model.get_db()
    cursor.execute(
        "DELETE FROM following "
        "WHERE username1 = %s "
        "AND username2 = %s;",
        (username1, username2)
    )


def like_unlike_or_comment(current_user):
    """Perform like, unlike, or comment actions."""
    if "like" in flask.request.form:
        like_post(current_user["username"], flask.request.form["postid"])

    elif "unlike" in flask.request.form:
        unlike_post(current_user["username"], flask.request.form["postid"])

    elif "comment" in flask.request.form:
        add_comment(current_user["username"], flask.request.form["postid"],
                    flask.request.form["text"])

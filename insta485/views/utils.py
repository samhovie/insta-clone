"""Insta485 view utility functions."""
from functools import wraps
import hashlib
import pathlib
import uuid

import flask
import insta485


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
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    users = cur.fetchall()

    # No users were found with the username.
    if len(users) != 1:
        return False

    [algorithm, salt, password_hash] = users[0]["password"].split("$")
    hash_obj = hashlib.new(algorithm)
    hash_obj.update((salt + password).encode("utf-8"))
    return hash_obj.hexdigest() == password_hash


def create_user(username, fullname, email, password, image_file):
    """Create a user with the given information."""
    connection = insta485.model.get_db()

    # If a user with this username already exists, raise a conflict error.
    cur = connection.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )
    if len(cur.fetchall()) != 0:
        flask.abort(409)

    # If no password is provided, raise a bad request error.
    if password == "":
        flask.abort(400)

    filename = save_upload(image_file)

    connection.execute(
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
    connection = insta485.model.get_db()

    if image_file is not None:
        delete_upload(old_file_name)
        filename = save_upload(image_file)
        connection.execute(
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
        connection.execute(
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
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username, fullname, email, filename FROM users "
        "WHERE username = ? AND created = ?",
        (flask.session["username"], flask.session["user_created"])
    )
    users = cur.fetchall()
    if len(users) != 1:
        del flask.session["username"]
        del flask.session["user_created"]
        return None
    return users[0]


def login(username):
    """Set cookies such that the current user is logged in as `username`."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT created FROM users WHERE username = ?",
        (username,)
    )
    users = cur.fetchall()
    if len(users) != 1:
        flask.abort(500)
    flask.session["username"] = username
    flask.session["user_created"] = users[0]["created"]


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


def remove_post(username, post_id):
    """Remove post_id if username is post owner."""
    connection = insta485.model.get_db()

    # Check if post exists and is owned by username, and also get post filename
    post_info = connection.execute(
        "SELECT owner, filename FROM posts "
        "WHERE postid = ?;",
        (post_id)
    ).fetchone()
    if post_info is None:
        flask.abort(404)
    elif username != post_info["owner"]:
        flask.abort(403)

    # Post exists and username owns it so delete all information for it
    connection.execute(
        "DELETE FROM posts "
        "WHERE postid = ?;",
        (post_id)
    )
    delete_upload(post_info["filename"])


def like_post(username, post_id):
    """Create entry for username liking post_id in likes."""
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES (?, ?);",
        (username, post_id)
    )


def unlike_post(username, post_id):
    """Remove entry for username liking post_id in likes."""
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM likes "
        "WHERE owner = ? AND postid = ?;",
        (username, post_id)
    )


def add_comment(username, post_id, text):
    """Add comment by username on post_id."""
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO comments (owner, postid, text) "
        "VALUES (?, ?, ?);",
        (username, post_id, text)
    )


def remove_comment(username, comment_id):
    """Remove comment_id if username is comment owner."""
    connection = insta485.model.get_db()

    # Check if comment exists and username is comment owner
    comment_owner = connection.execute(
        "SELECT owner FROM comments "
        "WHERE commentid = ?;",
        (comment_id)
    ).fetchone()
    if comment_owner is None:
        flask.abort(404)
    elif username != comment_owner["owner"]:
        flask.abort(403)

    # Comment exists and username owns it so delete it
    connection.execute(
        "DELETE FROM comments "
        "WHERE commentid = ?;",
        (comment_id)
    )

def unfollow(user1, user2):
    connection = insta485.model.get_db()

    connection.execute(
        "DELETE FROM following "
        "WHERE username1 = :user1 "
        "AND username2 = :user2;",
        {
            "user1": user1,
            "user2": user2,
        }
    )

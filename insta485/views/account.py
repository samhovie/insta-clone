"""
Insta485 accounts views.

URLs include:
/accounts/login/
/accounts/logout/
/accounts/create/
/accounts/delete/
/accounts/edit/
/accounts/password/
"""
import flask
import insta485
from insta485.views.utils import (
    create_hash,
    create_user,
    delete_upload,
    get_current_user,
    login,
    logout,
    requires_login,
    update_user,
    verify_credentials,
)


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display /accounts/login/ route."""
    current_user = get_current_user()
    if current_user is not None:
        return flask.redirect(flask.url_for("show_index"))
    if flask.request.method == "POST":
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        if not verify_credentials(username, password):
            flask.abort(403)
        login(username)
        return flask.redirect(flask.url_for("show_index"))
    context = {
        "current_user": current_user
    }
    return flask.render_template("login.html", **context)


@insta485.app.route('/accounts/logout/', methods=['POST'])
@requires_login
def show_logout():
    """Display /accounts/logout/ route."""
    logout()
    return flask.redirect(flask.url_for("show_login"))


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Display /accounts/create/ route."""
    current_user = get_current_user()
    if current_user is not None:
        return flask.redirect(flask.url_for("show_edit"))
    if flask.request.method == "POST":
        if not flask.request.files["file"]:
            flask.abort(400)
        create_user(
            username=flask.request.form["username"],
            fullname=flask.request.form["fullname"],
            email=flask.request.form["email"],
            password=flask.request.form["password"],
            image_file=flask.request.files["file"]
        )
        login(flask.request.form["username"])
        return flask.redirect(flask.url_for("show_index"))
    context = {
        "current_user": current_user
    }
    return flask.render_template("create.html", **context)


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
@requires_login
def show_delete():
    """Display /accounts/delete/ route."""
    current_user = get_current_user()
    if flask.request.method == "POST":
        cursor = insta485.model.get_db()

        # Delete all post images, and delete the profile picture.
        cursor.execute(
            "SELECT filename FROM posts WHERE owner = %s",
            (current_user["username"],)
        )
        for post in cursor.fetchall():
            delete_upload(post["filename"])
        delete_upload(current_user["filename"])

        # Delete the database entries.
        cursor.execute(
            "DELETE FROM users WHERE username = %s",
            (current_user["username"],)
        )

        # Log out the user.
        logout()

        return flask.redirect(flask.url_for("show_create"))
    context = {
        "current_user": current_user
    }
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
@requires_login
def show_edit():
    """Display /accounts/edit/ route."""
    current_user = get_current_user()
    if flask.request.method == "POST":
        image_file = None
        if flask.request.files["file"]:
            image_file = flask.request.files["file"]
        update_user(
            username=current_user["username"],
            fullname=flask.request.form["fullname"],
            email=flask.request.form["email"],
            old_file_name=current_user["filename"],
            image_file=image_file
        )
        current_user = get_current_user()
    context = {
        "current_user": current_user
    }
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
@requires_login
def show_password():
    """Display /accounts/password/ route."""
    current_user = get_current_user()
    if flask.request.method == "POST":
        old_password = flask.request.form["password"]
        if not verify_credentials(current_user["username"], old_password):
            flask.abort(403)

        new_password1 = flask.request.form["new_password1"]
        new_password2 = flask.request.form["new_password2"]
        if new_password1 != new_password2:
            flask.abort(401)

        new_hash = create_hash(new_password1)
        cursor = insta485.model.get_db()
        cursor.execute(
            "UPDATE users SET password = %s WHERE username = %s",
            (new_hash, current_user["username"])
        )
        return flask.redirect(flask.url_for("show_edit"))
    context = {
        "current_user": current_user
    }
    return flask.render_template("password.html", **context)

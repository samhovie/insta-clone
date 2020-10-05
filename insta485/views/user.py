"""
Insta485 user views.

URLs include:
/u/<user id>/
/u/<user id>/followers/
/u/<user id>/following/
"""
# import flask
import insta485
from insta485.views.utils import requires_login


@insta485.app.route('/u/<user_id>/')
@requires_login
def show_profile(user_id):
    """Display /u/<user_id>/ route."""
    return "Hello from user profile with id " + user_id + "!"


@insta485.app.route('/u/<user_id>/followers/')
def show_followers(user_id):
    """Display /u/<user_id>/followers/ route."""
    return "Hello from user followers with id " + user_id + "!"


@insta485.app.route('/u/<user_id>/following/')
def show_following(user_id):
    """Display /u/<user_id>/following/ route."""
    return "Hello from user following with id " + user_id + "!"

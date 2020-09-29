"""
Insta485 static file views.

URLs include:
/uploads/*
"""
import flask
import insta485
from insta485.views.utils import get_current_user


@insta485.app.route('/uploads/<path>')
def show_upload(path):
    """Return uploaded images."""
    if get_current_user() is None:
        flask.abort(403)
    return flask.send_from_directory(insta485.app.config["UPLOAD_FOLDER"],
                                     path)

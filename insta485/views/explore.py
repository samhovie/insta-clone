"""
Insta485 explore view.

URLs include:
/explore/
"""
# import flask
import insta485
from insta485.views.utils import requires_login


@insta485.app.route('/explore/')
@requires_login
def show_explore():
    """Display /explore/ route."""
    return "Hello, world from explore!"

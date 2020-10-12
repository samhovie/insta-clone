"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485

from insta485.views.utils import (
    get_current_user,
    requires_login,
)


@insta485.app.route('/', methods=['GET', 'POST'])
@requires_login
def show_index():
    """Display / route."""
    # Connect to database
    current_user = get_current_user()

    # Render home page template
    context = {
        'current_user': current_user,
    }
    return flask.render_template("index.html", **context)

"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485
# import insta485.views.utils
from insta485.views.utils import (
    requires_login,
    get_current_user,
    add_follower,
)


@insta485.app.route('/explore/', methods=['GET', 'POST'])
@requires_login
def show_explore():
    """Display /explore/ route."""
    # if 'username' in flask.session:
    connection = insta485.model.get_db()
    current_user = get_current_user()

    # context = {}
    if flask.request.method == 'POST':
        if flask.request.form.get('follow') is not None:
            add_follower(current_user['username'],
                         flask.request.form['username'])

    not_following = connection.execute(

        "SELECT * FROM users "
        "WHERE username NOT IN (SELECT username2 "
        "FROM following WHERE username1 = ? ) AND username != ?;",
        (current_user['username'], current_user['username'])

    )

    context = {'logname': current_user['username'],
               'current_user': current_user,
               'users': not_following, }
    return flask.render_template("explore.html", **context)

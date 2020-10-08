"""REST API for listing all available services."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=['GET'])
def get_services():
    """Return a list of all available REST API services.

    Example:
    {
      "posts": "/api/v1/p/",
      "url": "/api/v1/"
    }
    """
    context = {
      "posts": "/api/v1/p/",
      "url": "/api/v1/",
    }
    return flask.jsonify(**context)

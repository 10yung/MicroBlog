import flask

filters = flask.Blueprint('filters', __name__,template_folder='templates')


@filters.app_template_filter()
def pretty_date(value):
    """Format a date time to (Default): d Mon YYYY"""
    return value.strftime("%m-%d-%Y")

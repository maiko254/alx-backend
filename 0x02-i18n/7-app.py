#!/usr/bin/env python3
"""Flask app implementing locale translation"""
import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _, format_datetime
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime


class Config:
    """Supported languages definitions"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """Get the locale from the request or user preferred locale"""
    if 'locale' in request.args and request.args['locale'] in \
            app.config['LANGUAGES']:
        return request.args['locale']

    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Get the timezone from the request"""
    if 'timezone' in request.args:
        try:
            timezone = pytz.timezone(request.args['timezone'])
            return str(timezone)
        except UnknownTimeZoneError:
            pass

    if g.user and g.user.get('timezone'):
        try:
            timezone = pytz.timezone(g.user['timezone'])
            return str(timezone)
        except UnknownTimeZoneError:
            pass

    return 'UTC'


def get_user():
    """Get the user from the mock database"""
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set the current user before each request"""
    g.user = get_user()


@app.route('/')
def index():
    """Render the index.html template"""
    time = format_datetime(datetime.utcnow())
    return render_template('7-index.html', curr_time=time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

#!/usr/bin/env python3
"""Flask app implementing locale translation"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext as _

app = Flask(__name__)
babel = Babel(app, default_locale='en', default_timezone='UTC')

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """Get the locale from the request"""
    if 'locale' in request.args and request.args['locale'] in \
            app.config['LANGUAGES']:
        return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


class Config:
    """Supported languages definitions"""
    LANGUAGES = ["en", "fr"]


app.config.from_object(Config)


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
    title = _('Welcome to Holberton')
    header = _('Hello world!')
    return render_template('5-index.html',
                           home_title=title, home_header=header, user=g.user)


if __name__ == '__main__':
    app.run(debug=True)

#!/usr/bin/env python3
"""Flask app implementing locale translation"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext as _


class Config:
    """Supported languages definitions"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app, default_locale='en', default_timezone='UTC')


@babel.localeselector
def get_locale():
    """Get the locale from the request"""
    if 'locale' in request.args and request.args['locale'] in \
            app.config['LANGUAGES']:
        return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index.html template"""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

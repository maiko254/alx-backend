from flask import Flask, render_template, request
from flask_babel import Babel, gettext as _

app = Flask(__name__)
babel = Babel(app, default_locale='en', default_timezone='UTC')


@babel.localeselector
def get_locale():
    """Get the locale from the request"""
    if 'locale' in request.args and request.args['locale'] in \
            app.config['LANGUAGES']:
        return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


class Config:
    LANGUAGES = ["en", "fr"]


app.config.from_object(Config)


@app.route('/')
def index():
    """Render the index.html template"""
    title = _('Welcome to Holberton')
    header = _('Hello world!')
    return render_template('4-index.html',
                           home_title=title, home_header=header)


if __name__ == '__main__':
    app.run(debug=True)

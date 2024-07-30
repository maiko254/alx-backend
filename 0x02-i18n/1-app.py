from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)


def get_locale():
    """Get the locale from the request"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, default_locale='en', default_timezone='UTC')

class Config:
    LANGUAGES = ["en", "fr"]


@app.route('/')
def index():
    """Render the index.html template"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

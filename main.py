from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
import validators
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = '580cdbc914507569f2c2373e'
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(), nullable=False)
    shortened_url = db.Column(db.String(), nullable=False)


@app.route("/")
def index():
    return render_template('index.html', blinked_url=session.get('blinked_url'))

@app.route("/blink", methods=['POST'])
def shorten():
    if request.method == 'POST':
        url = request.form.get('url')
        if validators.url(url):
            base_url = request.url_root
            secret = secrets.token_hex(4)
            blinked_url = base_url + secret

            new_url = Url(original_url=url, shortened_url=blinked_url)
            db.session.add(new_url)
            db.session.commit()

            return render_template('blinked.html', blinked_url=blinked_url)
        else:
            flash('Not a valid URL')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route("/<url>", methods=['GET'])
def redirect_to_original(url):
    base_url = request.host_url
    search_url = base_url + url
    app.logger.debug(f"Searching for: {search_url}")

    redirect_entry = Url.query.filter_by(shortened_url=search_url).first()

    if redirect_entry:
        app.logger.debug(f"Found original URL: {redirect_entry.original_url}")
        return redirect(redirect_entry.original_url) 
    else:
        app.logger.debug("Shortened URL not found")
        flash('Shortened URL not found')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

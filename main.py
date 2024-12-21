from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import validators



app = Flask(__name__)
app.config['SECRET_KEY'] = '580cdbc914507569f2c2373e'
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/shorten", methods=['POST'])
def shorten():
    url = request.form.get('url')
    if validators.url(url):
        return render_template('index.html', url=url)
    else:
        flash('Not a valid URL')
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)

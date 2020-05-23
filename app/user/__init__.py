# Import flask and template operators
from functools import wraps

from flask import Flask, render_template, session, flash, redirect, url_for

# Import SQLAlchemy
#from flask import  SQL

# Define the WSGI application object
app = Flask(__name__)

# Configurations
#app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = None

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

#login Required decorator to protect users from routes
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'quizuser' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first","danger")
            return redirect(url_for('user.login_page'))

    return wrap
# Build the database:
# This will create the database file using SQLAlchemy
# db.create_all()

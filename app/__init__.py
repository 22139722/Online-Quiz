# Import flask and template operators
from flask import Flask, render_template
from flask import session
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy


# these files are for migrations
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager



# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


# Create Migrations Command
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

# set the upload folder
UPLOAD_FOLDER = 'uploads/'

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.admin.controller import admin_routes as admin_module
from app.user.controller import user_routes as user_module

# Register blueprint(s)
app.register_blueprint(admin_module)
app.register_blueprint(user_module)
# ..


# Build the database:
# This will create the database file using SQLAlchemy
#db.create_all()



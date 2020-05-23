from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import  app

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app.admin.models import *
from app.user.models import *

# Create Migrations Command
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()

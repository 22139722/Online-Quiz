# import secrets
#
# from flask import Flask, render_template, url_for, request, flash, redirect
#
#
# from flask_sqlalchemy import SQLAlchemy
#
#
# import os
# # these files are for migrations
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
#
# # Create Flask App Instance
# app = Flask(__name__)
#
# # These are the database Configurations
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///agile.sqlite3"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Create Migrations Command
# # by modules and controllers
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# manager = Manager(app)
#
# manager.add_command("db", MigrateCommand)
#
# # User Model To Store The User Information
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     is_admin = db.Column(db.Boolean, nullable=False)
#
#     def __init__(self, name=None, email=None, password=None, is_admin=False):
#         self.name = name
#         self.email = email
#         self.password = signals.generate_password(password)
#         self.is_admin = is_admin
#
#     def __repr__(self):
#         return '<User %r>' % self.name
#
#
# class Level(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), unique=True, nullable=False)
#     image = db.Column(db.String(120), unique=True, nullable=False)
#     priority = db.Column(db.Integer, unique=True, nullable=False)
#
#     def __repr__(self):
#         return '<Level %r>' % self.name
#
#
# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     level_id = db.Column(db.Integer, db.ForeignKey('level.id'),
#                          nullable=False)
#     level = db.relationship("Level",foreign_keys=level_id)
#     question = db.Column(db.Text, nullable=False)
#     answer_one = db.Column(db.Text, nullable=False)
#     answer_two = db.Column(db.Text, nullable=False)
#     answer_three = db.Column(db.Text, nullable=False)
#     answer_four = db.Column(db.Text, nullable=False)
#     correct = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         return '<Question %r>' % self.id
#
#
# # END MODELS
#
# class UserScoreBoard(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
#                         nullable=False)
#     test_time = db.Column(db.TIMESTAMP,nullable=False)
#     level_id = db.Column(db.Integer, db.ForeignKey('level.id'),
#                               nullable=True)
#
#
# class ScoreBoardDetail(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     scoreboard_id = db.Column(db.Integer, db.ForeignKey('user_score_board.id'),
#                         nullable=False)
#     level = db.Column(db.Text, nullable=False)
#     question = db.Column(db.Text, nullable=False)
#     answer_one = db.Column(db.Text, nullable=False)
#     answer_two = db.Column(db.Text, nullable=False)
#     answer_three = db.Column(db.Text, nullable=False)
#     answer_four = db.Column(db.Text, nullable=False)
#     correct = db.Column(db.Integer, nullable=False)
#     user_answer = db.Column(db.Integer, nullable=False)
#
#
#
#
# # set the secret key
# app.secret_key = secrets.token_hex(16)
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#
# # set the upload folder
# UPLOAD_FOLDER = 'uploads/'
# app.config['UPLOAD_FOLDER'] = "C:\\Users\\Karan\\PycharmProjects\\quizadmin\\static\\uploads"
#
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

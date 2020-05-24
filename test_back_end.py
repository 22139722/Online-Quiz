# tests/test_back_end.py
import os
import unittest
from unittest.mock import patch

from flask import abort, url_for
from flask_testing import TestCase

from app import db, app
from app.admin.models import Question, Level, User, LongTextQuestion, MCQQuestion, ShortTextQuestion
from config import BASE_DIR


class TestBase(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'test.sqlite3')
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = User(name="Admin", email="admin@gmail.com", password="admin@123", is_admin=True)

        # create test non-admin user
        user = User(name="User1", email="user1@gmail.com", password="user1@123")

        # save users to database
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()


class TestModels(TestBase):


    def test_user_model(self):
        """
        Test number of records in Employee table
        """
        self.assertEqual(User.query.count(), 2)

    def test_level_model(self):
        """
        Test number of records in Level table
        """

        # create level
        level = Level(name="IT", image="/abc.jpg", priority=1)

        # save department to database
        db.session.add(level)
        db.session.commit()
        self.level_id = level.id
        self.assertEqual(Level.query.count(), 1)

    def test_question_model(self):
        """
        Test number of questions in Question table
        """

        # create Long Text question
        question = Question()
        question.level_id = 1
        question.question_type = "long_text"
        db.session.add(question)
        db.session.commit()

        ques = LongTextQuestion()
        ques.question_id = question.id
        ques.question = "TestQuestion"
        db.session.add(ques)
        db.session.commit()

        # create Mcq Question
        question = Question()
        question.level_id = 1
        question.question_type = "mcq"
        db.session.add(question)
        db.session.commit()

        ques = MCQQuestion()
        ques.question_id = question.id
        ques.question = "TestQuestion"
        ques.answer_one = "TestOption1"
        ques.answer_two = "TestOption2"
        ques.answer_three = "TestOption3"
        ques.answer_four = "TestOption4"
        ques.correct = "1"
        db.session.add(ques)
        db.session.commit()

        # create Short Text Question
        question = Question()
        question.level_id = 1
        question.question_type = "fuzzy"
        db.session.add(question)
        db.session.commit()

        ques = ShortTextQuestion()
        ques.question_id = question.id
        ques.question = "TestQuestion"
        ques.answer = "TestAnswer"
        db.session.add(ques)
        db.session.commit()

        self.assertEqual(Question.query.count(), 3)
        self.assertEqual(MCQQuestion.query.count(), 1)
        self.assertEqual(ShortTextQuestion.query.count(), 1)
        self.assertEqual(LongTextQuestion.query.count(), 1)



class AdminTestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        target_url = self.client.get(url_for('admin.homepage'))
        redirect_url = url_for('admin.login')
        self.assertEqual(target_url.status_code, 302)
        self.assertRedirects(target_url, redirect_url)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('admin.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that Logout page is accessible without login
        """
        response = self.client.get(url_for('admin.admin_logout'))
        self.assertEqual(response.status_code, 302)

    # LEVELS TEST CASES
    def test_add_levels_view(self):
        """
        Test that addLevel page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.add_level')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_manage_levels(self):
        """
        Test that manageLevel page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.manage_levels')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_edit_levels(self):
        """
        Test that manageLevel page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.edit_level', id_='test')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_add_users(self):
        """
        Test that add user page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.add_user')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_manage_users(self):
        """
        Test that manage user page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.manage_users')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_edit_user_profile(self):
        """
        Test that edit user profile page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.edit_user_profile', id_="test")
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_change_user_password(self):
        """
        Test that change user password page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.change_user_password', id_="test")
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_scoreboard_view(self):
        """
        Test that User ScoreBoard is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.scoreboard')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_scoreboard_details_view(self):
        """
        Test that manage user ScoreBoard Details is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.scoreboard_detail', id_="test")
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_add_questions_view(self):
        """
        Test that Add Question is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.add_question')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_manage_questions_view(self):
        """
        Test that Manage Question is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.manage_questions')
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_edit_question_view(self):
        """
        Test that Manage Question is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('admin.edit_question', id_="test")
        redirect_url = url_for('admin.login')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class UserTestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        target_url = self.client.get(url_for('user.homepage'))
        redirect_url = url_for('user.login_page')
        self.assertEqual(target_url.status_code, 302)
        self.assertRedirects(target_url, redirect_url)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('user.login_page'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('user.logout')
        redirect_url = url_for('user.login_page')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    # def test_quiz_view(self):
    #     with patch("app.session", dict()) as session:
    #         """
    #         Test that QUiz is inaccessible without login
    #         and redirects to login page
    #         """
    #
    #         target_url = url_for('user.user_quiz', id_="test")
    #         redirect_url = url_for('user.login_page')
    #         response = self.client.get(target_url)
    #         assert session.get("username") == "1"
    #         self.assertEqual(response.status_code, 500)
    #         self.assertRedirects(response, redirect_url)

    def test_score_board_view(self):
        """
       Test that QUiz Scoreboard is inaccessible without login
       and redirects to login page
       """
        target_url = url_for('user.scoreboard', id_="test")
        redirect_url = url_for('user.login_page')
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

#
# class TestErrorPages(TestBase):
#
#     def test_403_forbidden(self):
#         # create route to abort the request with the 403 Error
#         @self.app.route('/403')
#         def forbidden_error():
#             abort(403)
#
#         response = self.client.get('/403')
#         self.assertEqual(response.status_code, 403)
#         self.assertTrue("403 Error" in response.data)
#
#     def test_404_not_found(self):
#         response = self.client.get('/nothinghere')
#         self.assertEqual(response.status_code, 404)
#         self.assertTrue("404 Error" in response.data)
#
#     def test_500_internal_server_error(self):
#         # create route to abort the request with the 500 Error
#         @self.app.route('/500')
#         def internal_server_error():
#             abort(500)
#
#         response = self.client.get('/500')
#         self.assertEqual(response.status_code, 500)
#         self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()

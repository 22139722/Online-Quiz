# tests/front_end_tests.py
import os,unittest,time

from flask import url_for
from flask_testing import LiveServerTestCase
from selenium import webdriver
from app import  db
from app.admin.models import User

# Set test variables for test admin user
from config import BASE_DIR

test_admin_name = "Admin"
test_admin_email = "admin@gmail.com"
test_admin_password = "admin@123"

# Set test variables for test user 1
test_user1_name = "User1"
test_user1_email = "user1@gmail.com"
test_user1_password = "user1@123"

# Set test variables for test user 1
test_user2_name = "User2"
test_user2_email = "user2@gmail.com"
test_user2_password = "user2@123"



BASE_URL = "http://127.0.0.1:8080"
class TestBase(unittest.TestCase):

    def setUp(self):
        """
        Will be called before every test
        """
        # create a new Chrome session
        self.driver = webdriver.Chrome(os.path.join(BASE_DIR,"chromedriver.exe"))


    def tearDown(self):

        db.session.remove()
        db.drop_all()
        db.create_all()
        # close the browser window
        self.driver.quit()
#



class UserRegistration(TestBase):
    register_url = (BASE_URL + "/register")
    def test_registration(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be
        redirected to the login page
        """

        self.driver.get(self.register_url)
        """
        # Click register menu link
        elem = self.driver.find_element_by_class_name("login-foot-nau")
        elem.find_elements_by_tag_name("a")[0].click()
        time.sleep(10)
        """

        # Fill in registration form
        self.driver.find_element_by_id("name").send_keys(test_user1_name)
        self.driver.find_element_by_id("email").send_keys(
            test_user1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_user1_password)
        self.driver.find_element_by_id("cpassword").send_keys(
            test_user1_password)

        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert self.register_url in self.driver.current_url

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "Signup Successfully" in success_message

        # Assert that there are now 1 employees in the database
        self.assertEqual(User.query.count(), 1)


    def test_registration_confirm_password(self):
        """
        Test that a user cannot register using an Already exist email message will be displayed
        """
        self.driver.get(self.register_url)
        # Fill in registration form
        self.driver.find_element_by_id("name").send_keys(test_user1_name)
        self.driver.find_element_by_id("email").send_keys(
            test_user1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_user1_password)
        self.driver.find_element_by_id("cpassword").send_keys(
            test_user2_password)

        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert self.register_url in self.driver.current_url

        # Assert success message is shown
        message = self.driver.find_element_by_class_name("alert").text
        assert "Password And Confirm Password Doesn't Match." in message


class UserLogin(TestBase):
    register_url = (BASE_URL + "/register")
    login_url = BASE_URL + "/login"
    def test_registration(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be
        redirected to the login page
        """

        self.driver.get(self.register_url)

        # Fill in registration form
        self.driver.find_element_by_id("name").send_keys(test_user1_name)
        self.driver.find_element_by_id("email").send_keys(
            test_user1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_user1_password)
        self.driver.find_element_by_id("cpassword").send_keys(
            test_user1_password)

        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert self.register_url in self.driver.current_url

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "Signup Successfully" in success_message

        # Assert that there are now 1 employees in the database
        self.assertEqual(User.query.count(), 1)

        #open Login Url
        self.driver.get(self.login_url)

        # Fill in Login form
        self.driver.find_element_by_id("email").send_keys(
            test_user1_email)
        self.driver.find_element_by_id("password").send_keys(
            test_user1_password)

        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)
        #assert if homepage is open
        assert BASE_URL in self.driver.current_url



if __name__ == '__main__':
    unittest.main()

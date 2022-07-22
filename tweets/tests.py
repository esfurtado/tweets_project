from cgi import test
from django.urls import reverse
from django.test import TestCase

from tweets.models import User

class RegistrationSubmitViewTests(TestCase):
    def test_happy_case(self):
        form_body = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "email@example.com",
            "username": "test_user",
            "password": "secretsecret",
            "confirm_password": "secretsecret",
        }
        #   When the client requests a post for the registration form we expect:
        #   - The response to return a 302 (redirect)
        #   - The response's header to be the login  url (if FAIL it will send a message)
        response = self.client.post(path=reverse("registration_submit"), data=form_body)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.headers["Location"], reverse("login"), msg="did not redirect to login page")
        
        # - The paramaters to be saved into the database
        # - Only one row should be saved
        query_result = User.objects.filter(username=form_body["username"])
        self.assertEquals(len(query_result), 1)

        # - When creating a new user, if username and email are different, it will save into database
        form_body2 = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "email2@example.com",
            "username": "test_user2",
            "password": "secretsecret",
            "confirm_password": "secretsecret",
        }

        self.client.post(path=reverse("registration_submit"), data=form_body2)
        query_result = User.objects.filter(username=form_body2["username"])
        self.assertEquals(len(query_result), 1)
    
    def test_validation_confirm_pass(self):
        form_body = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "email@example.com", #unique email
            "username": "test_user", #unique username
            "password": "secretsecret",
            "confirm_password": "secretsecret1",#different confirm_password
        }

        # If user has put a different string into confirm_password, show error message
        response = self.client.post(path=reverse("registration_submit"), data=form_body)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context['error'])
    
    def test_validation_unique_username(self):

        # If user inputs the same username, show error message
        form_body = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "email2@example.com", #unique email
            "username": "test_user", #same username
            "password": "secretsecret",
            "confirm_password": "secretsecret",#same confirm_password
        }

        self.client.post(path=reverse("registration_submit"), data=form_body)
        form_body["email"] = "email3@example.com"
        response = self.client.post(path=reverse("registration_submit"), data=form_body)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context['error'])

    def test_validation_unique_email(self):

        # If user inputs the same email as before, show error message
        form_body = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "email2@example.com", #same email
            "username": "test_user1", #unique username
            "password": "secretsecret",
            "confirm_password": "secretsecret", #same confirm_password
        }

        self.client.post(path=reverse("registration_submit"), data=form_body)
        form_body["username"] = "test_user"
        response = self.client.post(path=reverse("registration_submit"), data=form_body)
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response.context['error'])


        
        
import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.userModel import User
import copy


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

# LOGIN

    @patch('app.models.userModel.User.query')
    def test_login_successful(self, mock_query):
        # Test the successful login scenario:
        # - Mocks a user object in the database with login credentials.
        # - Sends a POST request to the '/login' endpoint with the login payload.
        # - Asserts that the response status code is 200.
        # - Checks that the response JSON contains the 'auth_token' and 'refresh_token' keys.

        mock_user = User(login='testuser', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_query.filter_by.return_value.first.return_value = mock_user
        payload = {
            'login': 'testuser',
            'password': 'Password123'
        }
        response = self.client.post('/login', data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.json)
        self.assertIn('refresh_token', response.json)

    @patch('app.models.userModel.User.query')
    def test_login_unsuccessful(self, mock_query):
        # Test an unsuccessful login scenario.
        # - Mocks a user object in the database with login credentials.
        # - Sends a POST request to the '/login' endpoint with incorrect login credentials.
        # - Asserts that the response status code is 401 (Unauthorized).
        # - Checks that the response JSON contains the expected error message.

        mock_user = User(login='testuser', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_query.filter_by.return_value.first.return_value = mock_user
        payload = {
            'login': 'testuser',
            'password': 'IncorrectPassword1'
        }
        response = self.client.post('/login', data=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Incorrect password"})

    @patch('app.models.userModel.User.query')
    def test_login_user_not_found(self, mock_query):
        # Test an unsuccessful login scenario when the user is not found.
        # - Mocks a user query in the database that returns None, indicating no user is found.
        # - Sends a POST request to the '/login' endpoint with login credentials.
        # - Asserts that the response status code is 404 (Not Found).
        # - Checks that the response JSON contains the expected error message.

        mock_query.filter_by.return_value.first.return_value = None
        payload = {
            'login': 'testuser',
            'password': 'Password123'
        }
        response = self.client.post('/login', data=payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'User not found'})

    @patch('app.models.userModel.User.query')
    def test_invalid_data(self, mock_query):
        # Test an unsuccessful login scenario when the login or password is not safe.
        # - Iterates over a payload dictionary and modifies each key to have an unsafe value.
        # - Sends a POST request to the '/login' endpoint with the modified payload.
        # - Asserts that the response status code is 404 (Not Found).
        # - Checks that the response JSON contains the expected error message.

        payload = {
            'login': 'tes',
            'password': 'IncorrectPassword1'
        }
        for x in payload:
            new_data = copy.deepcopy(payload)
            new_data[x] = "not"
            response = self.client.post('/login', data=new_data)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(
                response.json, {'error': 'Login or password is not safe'})

    @patch('app.models.userModel.User.query')
    def test_missing_data(self, mock_query):
        # Test an unsuccessful login scenario when the login or password is missing.
        # - Iterates over a payload dictionary and removes each key to simulate missing data.
        # - Sends a POST request to the '/login' endpoint with the modified payload.
        # - Asserts that the response status code is 404 (Not Found).
        # - Checks that the response JSON contains the expected error message.

        payload = {
            'login': 'teserrr',
            'password': 'IncorrectPassword1'
        }
        for x in payload:
            new_data = copy.deepcopy(payload)
            del new_data[x]
            response = self.client.post('/login', data=new_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json, {"error": "Request dont have all elements"})

# GET

    @patch('app.models.userModel.User.query')
    def test_user_not_found_get_all_users(self, mock_query):
        # Test retrieving all users when no user is found.
        # - Mocks a user query in the database that returns None, indicating no user is found.
        # - Sends a GET request to the '/users' endpoint.
        # - Asserts that the response status code is 200 (OK).
        mock_query.filter_by.return_value.all.return_value = None
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.userModel.User.query')
    def test_user_found_get_all_users(self, mock_query):
        # Test retrieving all users when users are found.
        # - Mocks a user query in the database that returns a list of mock users.
        # - Sends a GET request to the '/users' endpoint.
        # - Asserts that the response status code is 200 (OK).

        mock_user1 = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_user2 = User(login='testuser2', password='Password456',
                          first_name='John', last_name='Doe')
        mock_query.filter_by.return_value.all.return_value = [
            mock_user1, mock_user2]
        response = self.client.get('/user')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.userModel.User.query')
    def test_user_found_get_single_user(self, mock_query):
        # Test retrieving a single user when the user is found.
        # - Mocks a user query in the database that returns a mock user.
        # - Sends a GET request to the '/user/{id}' endpoint with a valid user ID.
        # - Asserts that the response status code is 200 (OK).

        mock_user = User(login='testuser', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_query.get.return_value = mock_user
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.userModel.User.query')
    def test_user_not_found_get_single_user(self, mock_query):
        # Test retrieving a single user when the user is not found.
        # - Mocks a user query in the database that returns None, indicating no user is found.
        # - Sends a GET request to the '/user/{id}' endpoint with a non-existing user ID.
        # - Asserts that the response status code is 404 (Not Found).
        mock_query.filter_by.return_value.first.return_value= None
        response = self.client.get('/user/1000')
        self.assertEqual(response.status_code, 404)

# ADD

    @patch('app.models.userModel.User.query')
    def test_missing_add_data(self, mock_query):
        # Test an unsuccessful user registration scenario when required data is missing.
        # - Iterates over a payload dictionary and removes each key to simulate missing data.
        # - Sends a POST request to the '/user/add' endpoint with the modified payload.
        # - Asserts that the response status code is 400 (Bad Request).
        # - Checks that the response JSON contains the expected error message.

        payload = {
            'login': 'tester',
            'password': 'CorrectPassword1',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'

        }
        for x in payload:
            new_data = copy.deepcopy(payload)
            del new_data[x]
            response = self.client.post('/user/add', data=new_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json, {"error": "Request dont have all elements"})

    @patch('app.models.userModel.User.query')
    def test_invalid_add_data(self, mock_query):
        # Test an unsuccessful user registration scenario when the data is invalid.
        # - Iterates over a payload dictionary and sets each key to an empty string to simulate invalid data.
        # - Sends a POST request to the '/user/add' endpoint with the modified payload.
        # - Asserts that the response status code is 400 (Bad Request).
        # - Checks that the respo   nse JSON contains the expected error message.

        payload = {
            'login': 'tester',
            'password': 'CorrectPassword1',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'
        }
        for x in payload:
            new_data = copy.deepcopy(payload)
            new_data[x] = ""
            response = self.client.post('/user/add', data=new_data)
            self.assertEqual(response.status_code, 404)

    @patch('app.models.userModel.User.query')
    def test_add_data(self, mock_query):
        # Test a successful user registration scenario when adding new user data.
        # - Mocks a user query in the database that returns None, indicating no existing user with the same login.
        # - Sets up a payload dictionary with valid user data.
        # - Mocks the database session using a context manager.
        # - Sends a POST request to the '/user/add' endpoint with the payload data.
        # - Asserts that the response status code is 200 (OK).
        # - Verifies that the database session was not called to add the user.

        mock_query.filter_by.return_value.first.return_value = None
        payload = {
            'login': 'tester',
            'password': 'CorrectPassword1',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': 0,
            'is_controller': 1
        }
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.post('/user/add', data=payload)
            self.assertEqual(response.status_code, 200)
            mock_session.assert_not_called()

    @patch('app.models.userModel.User.query')
    def test_add_data_exist(self, mock_query):
        # Test adding a user when a user with the same login already exists.
        # - Mocks the user query in the database to return a mock user with the same login.
        # - Sets up a payload dictionary with user data, including a login that already exists.
        # - Uses a context manager to patch the database session.
        # - Sends a POST request to the '/user/add' endpoint with the payload.
        # - Asserts that the response status code is 409 (Conflict).
        # - Asserts that the response JSON contains the expected error message.
        # - Asserts that the database session is not called, indicating that no user was added to the database.

        mock = User(login='tester', password='CorrectPassword1',
                          first_name='Jan', last_name='Kowalski')
        mock_query.filter_by.return_value.first.return_value = mock
        payload = {
            'login': 'tester',
            'password': 'CorrectPassword1',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'
        }
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.post('/user/add', data=payload)
            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.get_json(), {
                             "error": "Login already exist"})
            mock_session.assert_not_called()

# EDIT
    @patch('app.models.userModel.User.query')
    def test_missing_edit_data(self, mock_query):
        # Test editing a user when some data is missing.
        # - Sets up a payload dictionary with complete user data.
        # - Iterates over each key in the payload and creates a new data dictionary with one key removed.
        # - Sends a PUT request to the '/user/edit/{id}' endpoint with the modified data.
        # - Asserts that the response status code is 400 (Bad Request).
        # - Asserts that the response JSON contains the expected error message.

        payload = {
            'login': 'tester',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'

        }
        for x in payload:
            new_data = copy.deepcopy(payload)
            del new_data[x]
            response = self.client.put('/user/edit/1', data=new_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json,{"error":"Request don't have all elements"})

    @patch('app.models.userModel.User.query')
    def test_invalid_edit_data(self, mock_query):
        # Test an unsuccessful user edit scenario when the edited data is invalid.
        # - Creates a payload with valid user edit data.
        # - Iterates over the payload dictionary and sets each key to an empty string to simulate invalid data.
        # - Sends a PUT request to the '/user/edit/{id}' endpoint with the modified payload.
        # - Asserts that the response status code is 404 (Not Found).

        payload = {
            'login': 'tester',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'
        }
        for x in payload:
            new_data = copy.deepcopy(payload)
            new_data[x] = ""
            response = self.client.put('/user/edit/1', data=new_data)
            self.assertEqual(response.status_code, 404)

    @patch('app.models.userModel.User.query')
    def test_edit_data(self, mock_query):
        # Test an unsuccessful user edit scenario when the user is not found.
        # - Mocks a user query in the database that returns None, indicating no user is found.
        # - Creates a payload with valid user data for editing.
        # - Uses the context manager to patch the database session.
        # - Sends a PUT request to the '/user/edit/1' endpoint with the payload.
        # - Asserts that the response status code is 404 (Not Found).
        # - Asserts that the response JSON contains the expected error message.
        # - Asserts that the database session is not called.

        mock_query.filter_by.return_value.first.return_value = None
        payload = {
            'login': 'tester',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': 0,
            'is_controller': 1
        }
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.put('/user/edit/1', data=payload)
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json, {"error": "User not found"})
            mock_session.assert_not_called()

    @patch('app.models.userModel.User.query')
    def test_edit_data_exist(self, mock_query):
        # Test an unsuccessful user addition scenario when the user already exists.
        # - Mocks a user query in the database that returns an existing user.
        # - Creates a payload with user data for adding a new user.
        # - Uses the context manager to patch the database session.
        # - Sends a PUT request to the '/user/edit/1' endpoint with the payload.
        # - Asserts that the response status code is 200 (OK).
        # - Asserts that the response JSON contains the expected success message.
        # - Asserts that the database session is not called.

        mock = User(login='tester', password='CorrectPassword1',
                          first_name='Jan', last_name='Kowalski')
        mock_query.filter_by.return_value.first.return_value = mock
        payload = {
            'login': 'tester',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'
        }
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.put('/user/edit/1', data=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(),
                             {"message": "User changed successfully"})
            mock_session.assert_not_called()

# DEL
    @patch('app.models.userModel.User.query')
    def test_successfully_delete_user(self, mock_query):
        # Test the successful deletion of a user.
        # - Uses a context manager to patch the database session and the User.query.
        # - Creates a mock user and sets it as the return value of the User.query.
        # - Sends a DELETE request to the '/user/del/1' endpoint.
        # - Asserts that the response status code is 200 (OK).
        # - Asserts that the response JSON contains the expected success message.
        # - Asserts that the database session is not called, indicating that no user was deleted from the database.

        mock_user = User(login='testuser', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        payload = {
            'login': 'tester',
            'password': 'CorrectPassword1',
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'is_admin': '0',
            'is_controller': '0'
        }
        mock_query.filter_by.return_value.first.return_value = mock_user
        with patch('app.models.userModel.db.session') as mock_session:
            #self.client.post('/user/add', data=payload)
            response = self.client.delete('/user/del/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {"message": "User removed"})
            mock_session.assert_not_called()

    @patch('app.models.userModel.User.query')
    def test_not_delete_user_when_user_dont_exist(self, mock_query):
        # Test that a user is not deleted when the user does not exist.
        # - Uses a context manager to patch the database session and the User.query.
        # - Sets the return value of User.query.filter_by().first() to None, indicating no user is found.
        # - Sends a DELETE request to the '/user/del/10000' endpoint.
        # - Asserts that the response status code is 404 (Not Found).
        # - Asserts that the response JSON contains the expected error message.
        # - Asserts that the database session is not called, indicating no user deletion occurred.

        mock_query.filter_by.return_value.first.return_value = None
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.delete('/user/del/2137')
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.get_json(), {"error": "User not found"})


if __name__ == '__main__':
    unittest.main()

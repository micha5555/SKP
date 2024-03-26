import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.problematicCaseModel import ProblematicCase
from app.models.userModel import User
import copy
import io


class ProblematicCaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

# GET

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_not_found_get_all_cases(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test retrieving all problematic cases when no cases are found.
        # - Mocks a problematic case query in the database that returns None, indicating no cases are found.
        # - Sends a GET request to the '/problematicCase/' endpoint.
        # - Asserts that the response status code is 200 (OK).

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        mock_query.filter_by.return_value.all.return_value = None
        response = self.client.get(
            '/problematicCase/', headers={'Authorization': ''})
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_found_get_all_cases(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test retrieving all problematic cases when cases are found.
        # - Mocks a problematic case query in the database that returns a list of mock cases.
        # - Sends a GET request to the '/problematicCase/' endpoint.
        # - Asserts that the response status code is 200 (OK).

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        mock_case1 = ProblematicCase(registration="WA92829", creation_time="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                                     image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="99.7", status="NCH")
        mock_case2 = ProblematicCase(registration="WB98765", creation_time="2023-02-15T10:30:45Z", localization="-20.123456,-53.987654",
                                     image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="80.2", status="NCH")
        mock_query.filter_by.return_value.all.return_value = [
            mock_case1, mock_case2]
        response = self.client.get(
            '/problematicCase/', headers={'Authorization': ''})
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_found_get_single_case(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test retrieving a single problematic case when the case is found.
        # - Creates a mock problematic case object with sample data.
        # - Mocks a query in the database that returns the mock case when the get method is called.
        # - Sends a GET request to the '/problematicCase/{id}' endpoint with a valid case ID.
        # - Asserts that the response status code is 200 (OK).

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        mock = ProblematicCase(registration="WA92829", creation_time="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                               image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="99.7", status="NCH")
        mock_query.get.return_value = mock
        response = self.client.get(
            '/problematicCase/1', headers={'Authorization': ''})
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_not_found_get_single_case(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test the scenario of retrieving a single problematic case that is not found.
        # - Mocks the token data with an admin role, controller role, and user ID.
        # - Mocks a user query that returns a mock user object.
        # - Sends a GET request to the '/problematicCase/100' endpoint, assuming case ID 100 does not exist.
        # - Asserts that the response status code is 200 (OK).

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        response = self.client.get(
            '/problematicCase/100', headers={'Authorization': ''})
        self.assertEqual(response.status_code, 200)

# ADD

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_misssing_add_data(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test adding a problematic case when some data is missing.
        # - Creates a caseData dictionary with all the required data for adding a case.
        # - Loops through each key in caseData and creates a new_data dictionary with the same data, except for the current key being removed.
        # - Sends a POST request to the '/problematicCase/add' endpoint with the new_data.
        # - Asserts that the response status code is 400 (Bad Request).
        # - Asserts that the response JSON contains the expected error message.

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "image": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
            "probability":  "99.7",
            "controller_id": "1"
        }
        for x in caseData:
            new_data = copy.deepcopy(caseData)
            del new_data[x]
            response = self.client.post(
                '/problematicCase/add', data=new_data, headers={'Authorization': ''})
            self.assertEqual(response.status_code, 400)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_invalid_add_data(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test adding a problematic case with invalid data.
        # - Creates a caseData dictionary with all the required data for adding a case.
        # - Loops through each key in caseData and creates a new_data dictionary with the same data, except for the current key being set to an invalid value.
        # - Sends a POST request to the '/problematicCase/add' endpoint with the new_data.
        # - Asserts that the response status code is 400 (Bad Request) if the key is 'image', indicating an invalid image value.
        # - Asserts that the response status code is 406 (Not Acceptable) for other keys, indicating other invalid data.

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "probability":  "99.7",
            "controller_id": "1",
        }
        for x in caseData:
            new_data = copy.deepcopy(caseData)
            new_data[x] = ""
            response = self.client.post(
                '/problematicCase/add', data=new_data, headers={'Authorization': ''})
            if x in ["location", "probability", "datetime"]:
                self.assertEqual(response.status_code, 406)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_valid_add_data(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test the scenario of adding valid case data.
        # - Mocks the token data with an admin role, controller role, and user ID.
        # - Mocks a user query that returns a mock user object.
        # - Opens an image file in binary mode.
        # - Sets up the case data with valid values, including the image.
        # - Configures the problematic case query to return None, indicating no conflicting case.
        # - Asserts that the response status code is 202 (Accepted).
        # - Asserts that the database session is not called.

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        with open('img.jpg', 'rb') as image:
            caseData = {
                "register_plate": "WA92829",
                "datetime": "2023-01-12T19:12:30Z",
                "location": "-19.912086,-52.897761",
                "image": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
                "probability":  "99.7",
                "controller_id": "1",
                "image": image
            }
            with patch('app.models.problematicCaseModel.db.session') as mock_session:
                response = self.client.post(
                    '/problematicCase/add', data=caseData, headers={'Authorization': ''})
                self.assertEqual(response.status_code, 202)
                mock_session.assert_not_called()

# EDIT

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_valid_edit_data(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test the scenario of editing valid case data.
        # - Mocks the token data with an admin role, controller role, and user ID.
        # - Mocks a user query that returns a mock user object.
        # - Sets up the case data with valid values.
        # - Asserts that the response status code is 202 (Accepted).
        # - Asserts that the database session is not called.

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        caseData = {
            "registration": "WA92829",
            "status": "not_possible_to_check",
        }
        with patch('app.models.problematicCaseModel.db.session') as mock_session:
            response = self.client.put(
                '/problematicCase/edit/1', data=caseData, headers={'Authorization': ''})
            self.assertEqual(response.status_code, 202)
            mock_session.assert_not_called()

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_missing_edit_data(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test the scenario of editing case data with missing required fields.
        # - Mocks the token data with an admin role, controller role, and user ID.
        # - Mocks a user query that returns a mock user object.
        # - Sets up the case data with valid values.
        # - Iterates over each field in the case data and creates a new data dictionary without that field.
        # - Sends a PUT request to the '/problematicCase/edit/1' endpoint with the modified data.
        # - Asserts that the response status code is 400 (Bad Request).
        # - Asserts that the database session is not called.

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        caseData = {
            "registration": "WA92829",
            "status": "not_possible_to_check",
        }
        with patch('app.models.problematicCaseModel.db.session') as mock_session:
            for x in caseData:
                new_data = copy.deepcopy(caseData)
                del new_data[x]
                response = self.client.put(
                    '/problematicCase/edit/1', data=new_data, headers={'Authorization': ''})
                self.assertEqual(response.status_code, 400)
                mock_session.assert_not_called()

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_invalid_edit_data(self, mock_query, mock_getDataFromToken, mock_userQuery):
        # Test the scenario of editing case data with invalid values.
        # - Mocks the token data with an admin role, controller role, and user ID.
        # - Mocks a user query that returns a mock user object.
        # - Sets up the case data with valid values.
        # - Iterates over each field in the case data and creates a new data dictionary with an empty value for that field.
        # - Sends a PUT request to the '/problematicCase/edit/1' endpoint with the modified data.
        # - Asserts that the response status code is greater than or equal to 400 (Bad Request).
        # - Asserts that the database session is not called.

        mock_getDataFromToken.return_value = {
            'is_admin': True, 'is_controller': True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                         first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        caseData = {
            "registration": "WA92829",
            "status": "not_possible_to_check",
        }
        with patch('app.models.problematicCaseModel.db.session') as mock_session:
            for x in caseData:
                new_data = copy.deepcopy(caseData)
                new_data[x] = ""
                response = self.client.put(
                    '/problematicCase/edit/1', data=new_data, headers={'Authorization': ''})
                self.assertGreaterEqual(response.status_code, 400)
                mock_session.assert_not_called()


if __name__ == '__main__':
    unittest.main()

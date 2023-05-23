import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.problematicCaseModel import ProblematicCase
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

# GET

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_not_found_get_all_cases(self, mock_query):
        # Test retrieving all problematic cases when no cases are found.
        # - Mocks a problematic case query in the database that returns None, indicating no cases are found.
        # - Sends a GET request to the '/problematicCase/' endpoint.
        # - Asserts that the response status code is 200 (OK).

        mock_query.filter_by.return_value.all.return_value = None
        response = self.client.get('/problematicCase/')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_found_get_all_cases(self, mock_query):
        # Test retrieving all problematic cases when cases are found.
        # - Mocks a problematic case query in the database that returns a list of mock cases.
        # - Sends a GET request to the '/problematicCase/' endpoint.
        # - Asserts that the response status code is 200 (OK).

        mock_case1 = ProblematicCase(registration="WA92829", creation_time="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                                     image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="99.7", status="NCH")
        mock_case2 = ProblematicCase(registration="WB98765", creation_time="2023-02-15T10:30:45Z", localization="-20.123456,-53.987654",
                                     image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="80.2", status="NCH")
        mock_query.filter_by.return_value.all.return_value = [
            mock_case1, mock_case2]
        response = self.client.get('/problematicCase/')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_found_get_single_case(self, mock_query):
        # Test retrieving a single problematic case when the case is found.
        # - Creates a mock problematic case object with sample data.
        # - Mocks a query in the database that returns the mock case when the get method is called.
        # - Sends a GET request to the '/problematicCase/{id}' endpoint with a valid case ID.
        # - Asserts that the response status code is 200 (OK).

        mock = ProblematicCase(registration="WA92829", creation_time="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                               image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="99.7", status="NCH")
        mock_query.get.return_value = mock
        response = self.client.get('problematicCase/1')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_not_found_get_single_case(self, mock_query):
        # Test retrieving a single problematic case when the case is found.
        # - Mocks a problematic case query in the database that returns a mock case.
        # - Sends a GET request to the '/problematicCase/{id}' endpoint with a valid case ID.
        # - Asserts that the response status code is 200 (OK).

        mock_query.get.return_value = None
        response = self.client.get('problematicCase/10')
        self.assertEqual(response.status_code, 200)


# ADD

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_misssing_add_data(self, mock_query):
        # Test adding a problematic case when some data is missing.
        # - Creates a caseData dictionary with all the required data for adding a case.
        # - Loops through each key in caseData and creates a new_data dictionary with the same data, except for the current key being removed.
        # - Sends a POST request to the '/problematicCase/add' endpoint with the new_data.
        # - Asserts that the response status code is 400 (Bad Request).
        # - Asserts that the response JSON contains the expected error message.
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
            response = self.client.post('/problematicCase/add', data=new_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json, {"error": "request is missing"})

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_invalid_add_data(self, mock_query):
        # Test adding a problematic case with invalid data.
        # - Creates a caseData dictionary with all the required data for adding a case.
        # - Loops through each key in caseData and creates a new_data dictionary with the same data, except for the current key being set to an invalid value.
        # - Sends a POST request to the '/problematicCase/add' endpoint with the new_data.
        # - Asserts that the response status code is 400 (Bad Request) if the key is 'image', indicating an invalid image value.
        # - Asserts that the response status code is 406 (Not Acceptable) for other keys, indicating other invalid data.

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
            new_data[x] = ""
            response = self.client.post('/problematicCase/add', data=new_data)
            if x == "image":
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 406)

    #TODO
    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_invalid_add_data(self, mock_query):
        
        caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "image": "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
            "probability":  "99.7",
            "controller_id": "1"
        }
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.post('/problematicCase/add', data=caseData)
            self.assertEqual(response.status_code, 200)
            mock_session.assert_not_called()


    

# EDIT

# CORRECTION
    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_correction(self, mock_query):
        
        data = {
            'status':'check_if_paid_again'
        }
        mock = ProblematicCase(registration="WA92829", creation_time="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                               image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="99.7", status="NCH")
        mock_query.get.return_value = mock
        with patch('app.models.userModel.db.session') as mock_session:
            response = self.client.put('/problematicCase/correction/1', data=data)
            print(response)
            print(response.json)
            self.assertEqual(response.status_code, 200)
            mock_session.assert_not_called()


if __name__ == '__main__':
    unittest.main()

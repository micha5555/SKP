import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.notPaidCaseModel import NotPaidCase
from app.models.userModel import User
import copy

class notPaidTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

#GET
    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_case_not_found_get_all_cases(self, mock_query):
        mock_query.filter_by.return_value.all.return_value = None
        response = self.client.get('notPaidCase/')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_case_found_get_all_cases(self, mock_query):
        mock_case1 = NotPaidCase(registration="WA92829", date="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                                     filename="filename")
        mock_case2 = NotPaidCase(registration="WA92829", date="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                                     filename="filename")
        mock_query.filter_by.return_value.all.return_value = [
            mock_case1, mock_case2]
        response = self.client.get('notPaidCase/')
        self.assertEqual(response.status_code, 200)

#ADD
    @patch('app.auth.getDataFromToken')
    @patch('app.extensions.checkIfPaid')
    @patch('app.models.userModel.User.query')
    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_add_paid_case(self,mock_getDataFromToken,mock_checkIfPaid,mock_Userquery,mock_query):
        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_Userquery.filter_by.return_value.first.return_value = mock_user
        mock_checkIfPaid.return_value=False
        with open('img.jpg', 'rb') as image:
            caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "probability":  "99.7",
            "controller_id": "1",
            'image':image
            }
            with patch('app.models.userModel.db.session') as mock_session:
                    response = self.client.post('/notPaidCase/add', data=caseData,headers={'Authorization': ''})
                    self.assertEqual(response.status_code, 202)
                    mock_session.assert_not_called()

    @patch('app.auth.getDataFromToken')
    @patch('app.extensions.checkIfPaid')
    @patch('app.models.userModel.User.query')
    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_add_not_paid_case(self,mock_getDataFromToken,mock_checkIfPaid,mock_Userquery,mock_query):
        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_Userquery.filter_by.return_value.first.return_value = mock_user
        mock_checkIfPaid.return_value=True
        with open('img.jpg', 'rb') as image:
            caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "probability":  "99.7",
            "controller_id": "1",
            'image':image
            }
            with patch('app.models.userModel.db.session') as mock_session:
                    response = self.client.post('/notPaidCase/add', data=caseData,headers={'Authorization': ''})
                    self.assertEqual(response.status_code, 200)
                    mock_session.assert_not_called()

    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_missing_add_paid_case(self,mock_getDataFromToken,mock_Userquery,mock_query):
        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_Userquery.filter_by.return_value.first.return_value = mock_user
        caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "probability":  "99.7",
            "controller_id": "1",
            }
        with patch('app.models.userModel.db.session') as mock_session:
                for x in caseData:
                    if x != "controller_id":
                        new_data = copy.deepcopy(caseData)
                        del new_data[x]
                        response = self.client.post('/notPaidCase/add', data=new_data,headers={'Authorization': ''})
                        self.assertEqual(response.status_code, 400)
                        mock_session.assert_not_called()

    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_invalid_add_paid_case(self,mock_getDataFromToken,mock_Userquery,mock_query):
        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_Userquery.filter_by.return_value.first.return_value = mock_user
        caseData = {
            "register_plate": "WA92829",
            "datetime": "2023-01-12T19:12:30Z",
            "location": "-19.912086,-52.897761",
            "probability":  "99.7",
            "controller_id": "1"
            }
        with patch('app.models.userModel.db.session') as mock_session:
                for x in caseData:
                    if x != "controller_id":
                        new_data = copy.deepcopy(caseData)
                        new_data[x] = "not"
                        response = self.client.post('/notPaidCase/add', data=new_data,headers={'Authorization': ''})
                        self.assertGreaterEqual(response.status_code, 406)
                        self.assertLessEqual(response.status_code, 409)
                        mock_session.assert_not_called()

if __name__ == '__main__':
    unittest.main()
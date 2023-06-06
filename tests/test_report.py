import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.reportModel import Report
from app.models.userModel import User
import copy

class ReportTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

#GET
    @patch('app.models.reportModel.Report.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_not_found_get_all_cases(self, mock_query,mock_getDataFromToken,mock_userQuery):

        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        mock_query.filter_by.return_value.all.return_value= None
        with patch('app.models.reportModel.db.session') as mock_session:
            response = self.client.get('/report/',headers={'Authorization': ''})
            self.assertEqual(response.status_code, 200)

    @patch('app.models.reportModel.Report.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_get_all_cases(self, mock_query,mock_getDataFromToken,mock_userQuery):

        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        report=Report("2023-01-12T19:12:30Z", "2024-01-12T19:12:30Z", "filename", 1)
        mock_query.filter_by.return_value.all.return_value = [report]
        response = self.client.get('/report/',headers={'Authorization': ''})
        self.assertEqual(response.status_code, 200)


#ADD
    @patch('app.models.reportModel.Report.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_invalid_add_case(self, mock_query,mock_getDataFromToken,mock_userQuery):

        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        payload={"start_period":"2023-01-12T19:12:30Z",
        "end_period":"2023-08-12T19:12:30Z"}
        mock_query.filter_by.return_value.all.return_value = None
        for x in payload:
            new_data = copy.deepcopy(payload)
            new_data[x]=""
            response = self.client.post('/report/add', data=new_data,headers={'Authorization': ''})
            self.assertEqual(response.status_code, 404)

    @patch('app.models.reportModel.Report.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    def test_case_missing_add_case(self, mock_query,mock_getDataFromToken,mock_userQuery):

        mock_getDataFromToken.return_value = {'is_admin': True,'is_controller':True, 'id': 1}
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        payload={"start_period":"2023-01-12T19:12:30Z",
        "end_period":"2023-08-12T19:12:30Z"}
        mock_query.filter_by.return_value.all.return_value = None
        for x in payload:
            new_data = copy.deepcopy(payload)
            del new_data[x]
            response = self.client.post('/report/add', data=new_data,headers={'Authorization': ''})
            self.assertEqual(response.status_code, 400)

    @patch('app.models.reportModel.Report.query')
    @patch('app.auth.getDataFromToken')
    @patch('app.models.userModel.User.query')
    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    @patch('app.models.notPaidCaseModel.NotPaidCase.query')
    def test_case_add_case(self, mock_query,mock_getDataFromToken,mock_userQuery,mock_problematic,mock_notPaid):

        usr={'is_admin': True,'id': 1}
        mock_getDataFromToken.return_value = usr
        mock_user = User(login='testuser1', password='Password123',
                          first_name='Jan', last_name='Kowalski')
        mock_userQuery.get.return_value = mock_user
        payload={"start_period":"2023-01-12T19:12:30Z",
        "end_period":"2023-08-12T19:12:30Z"}
        mock_query.filter_by.return_value.all.return_value = None
        mock_problematic.query.filter.all.return_value=[]
        mock_notPaid.query.filter.all.return_value=[]
        with patch('app.models.reportModel.db.session') as mock_session:
            response = self.client.post('/report/add', data=payload,headers={'Authorization': ''})
            self.assertEqual(response.status_code, 200)
if __name__ == '__main__':
    unittest.main()
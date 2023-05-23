import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.notPaidCaseModel import NotPaidCase
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

#GET

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_not_found_get_all_cases(self, mock_query):

        mock_query.filter_by.return_value.all.return_value = None
        response = self.client.get('/problematicCase/')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_found_get_all_cases(self, mock_query):

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

        mock = ProblematicCase(registration="WA92829", creation_time="2023-01-12T19:12:30Z", localization="-19.912086,-52.897761",
                               image="iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==", probability="99.7", status="NCH")
        mock_query.get.return_value = mock
        response = self.client.get('problematicCase/1')
        self.assertEqual(response.status_code, 200)

    @patch('app.models.problematicCaseModel.ProblematicCase.query')
    def test_case_not_found_get_single_case(self, mock_query):
        mock_query.get.return_value = None
        response = self.client.get('problematicCase/10')
        self.assertEqual(response.status_code, 200)


#ADD


if __name__ == '__main__':
    unittest.main()
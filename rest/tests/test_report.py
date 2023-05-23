import unittest
from unittest.mock import patch
from flask import Flask
from app import app
from app.models.reportModel import Report
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

#ADD

#DOWNLOAD

if __name__ == '__main__':
    unittest.main()
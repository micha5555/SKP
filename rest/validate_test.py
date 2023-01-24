import unittest
from flaskr.validate import validateUsernameAndPassword

class ValidateTest(unittest.TestCase):
    def test_ReturnFalseWhenUsernameIsEmpty(self):
        username=""
        password="12345678"
        self.assertFalse(validateUsernameAndPassword(username,password))

    def test_ReturnFalseWhenPasswordIsEmpty(self):
        username="ab12"
        password=""
        self.assertFalse(validateUsernameAndPassword(username,password))

    def test_ReturnFalseWhenPasswordIsToShort(self):
        username="ab12"
        password="1234"
        self.assertFalse(validateUsernameAndPassword(username,password))
    
    def test_ReturnFalseWhenUsernameContainsSpecialCharacter(self):
        username="ab*12"
        password="1234asdf"
        self.assertFalse(validateUsernameAndPassword(username,password))

    def test_ReturnFalseWhenPasswordContainsSpecialCharacter(self):
        username="ab12"
        password="qwertyuio*"
        self.assertFalse(validateUsernameAndPassword(username,password))

    def test_ReturnFalseWhenUsernameContainsSQLCommand(self):
        username="DROP"
        password="1234asdf"
        self.assertFalse(validateUsernameAndPassword(username,password))

    def test_ReturnFalseWhenPasswordContainsSQLCommand(self):
        username="ab12"
        password="CREATEadb"
        self.assertFalse(validateUsernameAndPassword(username,password))

    def test_ReturnTrueWhenPasswordAndUsernameAreOK(self):
        username="admin"
        password="admin123"
        self.assertTrue(validateUsernameAndPassword(username,password))

if __name__ == '__main__':
    unittest.main()
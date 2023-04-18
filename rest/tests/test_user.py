import unittest
import copy
from app import create_app

def send_login_request(app,user_data,expeted_data,status_code):
    response = app.client.post('/user/login', json=user_data)
    app.assertEqual(response.status_code, status_code)
    app.assertEqual(response.get_json(),expeted_data)


class UserTest(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()

    def addTester(self):
        tester_data = {
            "login": "tester",
            "password": "Admin123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_admin":"0",
            "is_controller":"1"
        }
        self.client.post('/user/add', json=tester_data)

    def tearDown(self):
        user_data = {
            "login": "tester",
        }
        self.client.delete('/user/del', json=user_data)
        user_data = {
            "login": "uzytkownikTestowy",
        }
        self.client.delete('/user/del', json=user_data)


    #login
    def test_request_login_without_username(self):
        user_data = {
            'password': 'test_password'
        }
        expeted_data={"error":"Request dont have all elements"}
        send_login_request(self,user_data,expeted_data,400)

    def test_request_login_without_password(self):
        user_data = {
            'login': 'testPassword'
        }
        expeted_data={"error":"Request dont have all elements"}
        send_login_request(self,user_data,expeted_data,400)

    def test_request_login_with_inappropriate_login(self):
        user_data = {
            "login": "",
            "password": "testPassword123"
        }
        expeted_data={"error":"Login or password is not safe"}
        send_login_request(self,user_data,expeted_data,404)

    def test_request_login_with_inappropriate_password(self):
        user_data = {
            "login": "loginBardzoFajny",
            "password": ""
        }
        expeted_data={"error":"Login or password is not safe"}
        send_login_request(self,user_data,expeted_data,404)
    
    def test_request_login_when_login_not_exist(self):
        user_data = {
            "login": "loginBardzoFajny",
            "password": "Haslo123"
        }
        expeted_data={"error":"User not found"}
        send_login_request(self,user_data,expeted_data,404)
    
    def test_request_login_when_password_is_wrong(self):
        self.addTester()
        user_data = {
            "login": "tester",
            "password": "Haslo123"
        }
        expeted_data={"error":"Incorrect password"}
        send_login_request(self,user_data,expeted_data,404)

    def test_requestSuccessfullyLoginWhenUserExists(self):
        self.addTester()
        user_data = {
            "login": "tester",
            "password": "Admin123"
        }
        response = self.client.post('/user/login', json=user_data)
        self.assertEqual(response.status_code, 200)

    #user get
    def test_requestGetAllUsers(self):
        response = self.client.get('/user/users')
        self.assertEqual(response.status_code, 200)

    def test_requestGetUser(self):
        response = self.client.get('/user/get/1')
        self.assertEqual(response.status_code, 200)
    
    def test_requestGetNotExistingUser(self):
        response = self.client.get('/user/get/10000')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(),{"error":"User not found"})

    #user add
    def test_requestSuccessfullyAddNewUserAndTryToAddHimAgain(self):
        user_data = {
            "login": "uzytkownikTestowy",
            "password": "Admin123",
            "first_name": "Alina",
            "last_name": "Nowak",
            "is_admin":"1",
            "is_controller":"0"
        }
        response = self.client.post('/user/add', json=user_data)
        self.assertEqual(response.status_code, 200)
        responseNext = self.client.post('/user/add', json=user_data)
        self.assertEqual(responseNext.status_code, 404)
        self.assertEqual(responseNext.get_json(),{"error":"Login already exist"})

    def test_requestShouldNotAddUserWithoutNecessaryElemensts(self):
        user_data = {
            "login": "tester",
            "password": "Admin123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_admin":"0",
            "is_controller":"1"
        }
        for x in user_data:
            new_data=copy.deepcopy(user_data)
            del new_data[x]
            response = self.client.post('/user/add', json=new_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),{"error":"Request dont have all elements"})

    def test_requestShouldNotAddUserwithoutValidateAllElems(self):
        user_data = {
            "login": "tester",
            "password": "Admin123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_admin":"0",
            "is_controller":"1"
        }
        for x in user_data:
            new_data=copy.deepcopy(user_data)
            new_data[x]=""
            response = self.client.post('/user/add', json=new_data)
            if(x == "login" or x == "password"):
                self.assertEqual(response.get_json(),{"error":"Login or password is not safe"})
                self.assertEqual(response.status_code, 404)
            elif(x == "first_name" or x == "last_name"):
                self.assertEqual(response.get_json(),{"error":"Firstname or surname is not correct"})
                self.assertEqual(response.status_code, 404)
            elif(x == "is_admin" or x == "is_controller"):
                self.assertEqual(response.status_code, 200)
                self.client.delete('/user/del', json={"login":"tester"})
    #edit
    def test_request_successfully_edit_user(self):
        self.addTester()
        user_data = {
            "login": "tester",
            "password": "Admin123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_admin":"0",
            "is_controller":"1"
        }
        response = self.client.patch('/user/edit/1', json=user_data)
        self.assertEqual(response.status_code, 200)

    def test_requestShouldNotEditUserwithoutValidateAllElems(self):
        user_data = {
            "login": "tester",
            "password": "Admin123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_admin":"0",
            "is_controller":"1"
        }
        self.addTester()
        for x in user_data:
            new_data=copy.deepcopy(user_data)
            new_data[x]=""
            response = self.client.patch('/user/edit', json=new_data)
            if(x == "login" or x == "password"):
                self.assertEqual(response.get_json(),{"error":"Login or password is not safe"})
                self.assertEqual(response.status_code, 404)
            elif(x == "first_name" or x == "last_name"):
                self.assertEqual(response.get_json(),{"error":"Firstname or surname is not correct"})
                self.assertEqual(response.status_code, 404)
            elif(x == "is_admin" or x == "is_controller"):
                self.assertEqual(response.status_code, 200)

    def test_requestShouldNotEditUserWithoutNecessaryElemensts(self):
        user_data = {
            "login": "tester",
            "password": "Admin123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "is_admin":"0",
            "is_controller":"1"
        }
        for x in user_data:
            new_data=copy.deepcopy(user_data)
            del new_data[x]
            response = self.client.patch('/user/edit', json=new_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),{"error":"Request dont have all elements"})
        
    #del
    def test_requestSuccessfullyDeleteUser(self):
        self.addTester()
        response = self.client.delete('/user/del/2', json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),{"message":"User removed"})

    def test_requestShouldNotDeleteUserWhenUserDontExist(self):
        user_data = {
            "login": "tester",
        }
        response = self.client.delete('/user/del/10000', json=user_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(),{"error":"User not found"})

if __name__ == '__main__':
    unittest.main()
import unittest
from app import create_app

class ProblematicCaseTest(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()

    def test_request(self):
        response = self.client.get('/problematicCase/')
        self.assertEqual(response.status_code, 200)
    
    def test_requestGetFirst(self):
        response = self.client.get('/problematicCase/1')
        self.assertEqual(response.status_code, 200)
    def test_requestGetNotExist(self):
        response = self.client.get('/problematicCase/10000')
        self.assertEqual(response.status_code, 200)
    
    def test_requestAdd(self):
        caseData = {
        "register_plate":"WA92829",
        "datetime" :"2023-01-12T19:12:30Z",
        "location":"-19.912086,-52.897761" ,
        "image" :"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
        "probability":"99.7", 
        "controller_id":"1"  
        }
        response = self.client.post('/problematicCase/add',json=caseData)
        self.assertEqual(response.status_code, 200)

    def test_requestShouldNotAddCaseWhenNotValidateData(self):
        caseData = {
        "register_plate":"WA92829",
        "datetime" :"2023-01-12T19:12:30Z",
        "location":"-19.912086,-52.897761" ,
        "image" :"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
        "probability":" 99.7", 
        "controller_id":"1"  
        }
        for x in caseData:
            newData=copy.deepcopy(caseData)
            newData[x]="veryLongRandomStringThatShouldWork"
            response = self.client.post('/problematicCase/add', json=newData)
            self.assertEqual(response.status_code, 406)

    def test_requestShouldNotAddCaseWithoutNecessaryElemensts(self):
        caseData = {
        "register_plate":"WA92829",
        "datetime" :"2023-01-12T19:12:30Z",
        "location":"-19.912086,-52.897761" ,
        "image" :"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
        "probability":" 99.7", 
        "controller_id":"1"  
        }
        for x in caseData:
            newData=copy.deepcopy(caseData)
            del newData[x]
            response = self.client.post('/problematicCase/add', json=newData)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),{"error": "request is missing"})

    def test_requestEdit(self):
        caseData = {
        "id":"1",
        "registration":"WA92829",
        "administration_edit_time" :"2023-01-12T19:12:30Z",
        }
        response = self.client.put('/problematicCase/edit',json=caseData)
        self.assertEqual(response.status_code, 200)

    def test_requestEdit(self):
        caseData = {
        "id":"1",
        "registration":"WA92829",
        "administration_edit_time" :"2023-01-12T19:12:30Z",
        }
        for x in caseData:
            newData=copy.deepcopy(caseData)
            del newData[x]
            response = self.client.post('/problematicCase/add', json=newData)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),{"error": "request is missing"})

    def test_requestEdit(self):
        caseData = {
        "id":"1",
        "registration":"WA92829",
        "administration_edit_time" :"2023-01-12T19:12:30Z",
        }
        for x in caseData:
            newData=copy.deepcopy(caseData)
            newData[x]="veryLongRandomStringThatShouldWork"
            response = self.client.post('/problematicCase/add', json=newData)
            self.assertEqual(response.status_code, 406)

    def test_requestShouldCorrectionCase(self):
        caseData = {
        "id":"1",
        "status":"not_possible_to_check",
        "admin_id":"1"  
        }
        response = self.client.post('/problematicCase/correction', json=caseData)
        self.assertGreaterEqual(response.status_code, 200)
        self.assertLess(response.status_code, 202)

    def test_requestShouldCorrectionCase(self):
        caseData = {
        "id":"1",
        "status":"not_possible_to_check",
        "admin_id":"1"  
        }
        for x in caseData:
            newData=copy.deepcopy(caseData)
            newData[x]="veryLongRandomStringThatShouldWork"
            response = self.client.post('/problematicCase/correction', json=newData)
            self.assertEqual(response.status_code, 406)

    def test_requestShouldCorrectionCase(self):
        caseData = {
        "id":"1",
        "status":"not_possible_to_check",
        "admin_id":"1"  
        }
        for x in caseData:
            newData=copy.deepcopy(caseData)
            del newData[x]
            response = self.client.post('/problematicCase/correction', json=newData)
            self.assertEqual(response.status_code, 406)


if __name__ == '__main__':
    unittest.main()
        
        
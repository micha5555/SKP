import unittest
import copy
from app import create_app

class notPaidCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()

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
            response = self.client.post('/notPaidCase/add', json=newData)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),{"error": "request is missing"})

    def test_requestShouldAddCase(self):
        caseData = {
        "register_plate":"WA92829",
        "datetime" :"2023-01-12T19:12:30Z",
        "location":"-19.912086,-52.897761" ,
        "image" :"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAMUlEQVR4nGIp5n3CgA1MYP+JVZwJqygeMKqBGMDI6ZGCVaL9lCF1bBjVQAwABAAA//9W/wVNpn8uyAAAAABJRU5ErkJggg==",
        "probability":"99.7", 
        "controller_id":"1"  
        }
        response = self.client.post('/notPaidCase/add', json=caseData)
        self.assertGreaterEqual(response.status_code, 200)
        self.assertLess(response.status_code, 202)

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
            response = self.client.post('/notPaidCase/add', json=newData)
            self.assertEqual(response.status_code, 406)

if __name__ == '__main__':
    unittest.main()
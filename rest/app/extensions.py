import datetime
import random
import base64
import uuid
from datetime import datetime
import os
from PIL import Image
from io import BytesIO
from config import Config


def tokenAdminRequire():
    pass

def tokenControlerRequire():
    pass

def createToken():
    pass

def getDataFromToken():
    pass

# We get time from UTC,, but we need Poland time zone so we need to add +1 to hour
def createDatetime(string):
    dt_utc = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    dt_local = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
    return dt_local

# We get current time from UTC,, but we need Poland time zone so we need to add +1 to hour
def getDatetimeNow():
    dt_utc = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    dt_local = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=1)))
    return dt_local

def allElementsInList(elements, lst):
    return all(element in lst for element in elements)

def checkIfPaid(registration, detection_time):
    # here will be created element which will check if element was paid or not 
    checked = random.random()*100
    if checked > 20:
        return True
    return False

def create_image(base64encoded):
    return base64.b64decode(base64encoded)

def create_image_name():
    file_uuid = uuid.uuid4()
    now = datetime.now()
    return f"{file_uuid}_{now.strftime('%Y5m%d_%H%M%S')}"

def save_image_to_local(image, file_name):
    with BytesIO(image) as f:
        save_image = Image.open(f)
        save_image.save(os.path.join(os.getcwd(), Config.UPLOAD_FOLDER, file_name), format="PNG")
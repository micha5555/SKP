class Config:
  SECRET_KEY = '52829798f03c4410b085a4b385b1fa6d'
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@172.23.23.23:3306/skp_test'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = '/upload'
  STATIC_URL_PATH = ''
  STATIC_FOLDER = 'static'

  # state of problematic case
  NOT_CHECKED = 'NCH' # waiting to checked
  CHECKED_TO_PAID = 'CTP' # check and not paid  
  CHECKED_OK = 'COK' # checked and paid
  CHECKED_NOT_CONFIRMED = 'CNC' # check and not possible to checked
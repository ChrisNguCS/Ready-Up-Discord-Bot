from pprint import pprint
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret_224277258275-nhp08f5ghdhqs5bme4v2lvsoq0r5nvhe.apps.googleusercontent.com.json'
API_NAME = 'PythonCalendarAPI'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient import discovery

CREDENTIALS_FILE = 'rich-atom-374718-5d92b2c58bb5.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

EMAIL_USER = 'sihuannewrise@gmail.com'
FORMAT = '%Y/%m/%d %H:%M:%S'

def auth():
    credentials = Credentials.from_service_account_file(
        filename=CREDENTIALS_FILE, scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service, credentials

def create_spreadsheet(service):
    sheet_title = datetime.now().strftime(FORMAT)
    spreadsheet_body = {
        'properties': {
            'title': 'Morelia viridis menu',
            'locale': 'ru_RU',
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': sheet_title,
                'gridProperties': {
                    'rowCount': 20,
                    'columnCount': 11,
                }
            }
        }]
    }
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheet_id = response['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
    return spreadsheet_id

def set_user_permissions(spreadsheetId, credentials):
    permissions_body={'type': 'user',
                      'role': 'writer',
                      'emailAddress': EMAIL_USER}
    
    drive_service = discovery.build('drive', 'v3', credentials=credentials)
    
    drive_service.permissions().create(
        fileId=spreadsheetId,
        body=permissions_body,
        fields='id'
    ).execute()

service, credentials = auth()
spreadsheetId = create_spreadsheet(service)
set_user_permissions(spreadsheetId, credentials)

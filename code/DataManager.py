from __future__ import print_function
import pickle
import os.path
from apiclient import errors

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# https://developers.google.com/sheets/api/guides/authorizing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1rR9e5xfW942puPeY0wIu6xlfltC5k-8s2vbNpMFMs94'
RANGE_NAME = '10ª semana!A:Z'
TAB_ID = 1335269956


def get_sheets_service():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('..\\credentials\\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '..\\credentials\\client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('..\\credentials\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def get_drive_service():
    """Shows basic usage of the Drive v3 API.
      Prints the names and ids of the first 10 files the user has access to.
      """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('..\\credentials\\token.pickle'):
        with open('..\\credentials\\token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '..\\credentials\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('..\\credentials\\token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def apply_id(service):
    # Call the Sheets API
    sheet = service.spreadsheets()
    my_range = [{
        'sheetId': TAB_ID,
        'startRowIndex': 1,
        'endRowIndex': 1000,
        'startColumnIndex': 0,
        'endColumnIndex': 0,
    }]
    values = [
            '=HYPERLINK("https://docs.google.com/spreadsheets/d/1g7CrKmY5fdYobDURXT3L7FjO6JgzIkLg1Y80UjO8-CM/edit#gid=2131381500&range=A" & ROW() & ":K" & ROW(),ROW()-1)'
    ]
    data = {
            'range': my_range,
            'values': values
        }

    body = {
        # 'valueInputOption': value_input_option,
        'data': data
    }
    result = sheet.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))


def get_values(service):
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)


def get_files(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def get_folders(service, folder_id):
    """Print files belonging to a folder.

    Args:
        service: Drive API service instance.
        folder_id: ID of the folder to print files from.
    """
    page_token = None
    while True:
        response = service.files().list(q="mimeType='application/vnd.google-apps.folder' "
                                          "and '%s' in parents" % folder_id,
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            print('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break


if __name__ == '__main__':
    # service = get_sheets_service()
    # get_values(service)
    # apply_id(service)
    service = get_drive_service()
    # get_files(service)
    get_folders(service, '1zluJksEAjLJm0WUSCPdCPsOWLrJygLlT')
    get_folders(service, '15NLJ_0Zp_6Bv2S2aXC6adrL_0jQJHkYi')


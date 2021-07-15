# https://developers.google.com/sheets/api/quickstart/python

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
RANGE_NAME = "A:C"


class SpreadSheet:
    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token_spreadsheet.json'):
            creds = Credentials.from_authorized_user_file('token_spreadsheet.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token_spreadsheet.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('sheets', 'v4', credentials=creds)
        self.sheet = self.service.spreadsheets()

    def get_data(self):
        result = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                         range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found')
            return []

        return values

    def write_value(self, range_name="C1:C1", values=[[1]]):
        body = {'values': values}
        try:
            result = self.sheet.values().update(
                spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption='RAW', body=body
            ).execute()
            return True
        except Exception as e:
            print(f'SpreadSheet Write Error: {e}')
            return False



if __name__ == '__main__':
    sheet = SpreadSheet()
    print(sheet.get_data())
    sheet.write_value("C2:C2", [[1]])


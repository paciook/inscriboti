import os.path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1SVEIbG5q_UVfa-eWMuo_b8OdF_LNjmPjV6vQ7dpt62Y'
RANGE_NAME = 'Alumnos!A1:H100'

class Datasheet():
    def __init__(self, creds_path):

        if os.path.exists(creds_path):
            credentials = Credentials.from_service_account_file(
                filename=creds_path,
                scopes=SCOPES
            )

        try:
            self.service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                        range=RANGE_NAME).execute()
            self.values = result.get('values', [])

            if not self.values:
                print('No data found.')
                return

            self.alumnos = {0: "Ejemplo"}

            for row in self.values[1:]:
                if(row == []):
                    break
                self.alumnos.update({int(row[1]): row[0]})


        except HttpError as err:
            print(err)

    def doesExist(self, padron):
        return (padron in self.alumnos)

    def getName(self, padron):
        return self.alumnos.get(padron)

    def inDiscord(self, padron):
        for row in self.values[1:]:
            if row == []:
                break
            
            if(padron != int(row[1])):
                continue
            row.append('A')
            row.append('A')
            row[5] = 'D'
        
        body = {'values': self.values}

        result = self.service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption="USER_ENTERED", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
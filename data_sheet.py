import os.path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
RANGE_NAME = 'Alumnos!A1:G100' # Hardcodeado por ahora porque ni idea como cambiarlo

class Datasheet():
    def __init__(self, creds_path, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        
        credentials = None
        if os.path.exists(creds_path):
            credentials = Credentials.from_service_account_file(
                filename=creds_path,
                scopes=SCOPES
            )

        try:
            self.service = build('sheets', 'v4', credentials=credentials)

            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheetId,
                                        range=RANGE_NAME).execute()
            self.values = result.get('values', [])

            if not self.values:
                print('No data found.')
                return

            self.alumnos = {}

            header = self.values[0]
            for row in self.values[1:]: # Skip the first as is the header
                if(row == []):
                    break
                self.alumnos.update({int(row[header.index('Padrón')]): row[header.index('Nombre')]})


        except HttpError as err:
            print(err)

    def doesExist(self, padron):
        return (padron in self.alumnos)

    def getName(self, padron):
        return self.alumnos.get(padron)

    def loggedInDiscord(self, padron, text='D'):
        for row in self.values[1:]:
            if row == []:
                break
            
            if(padron != int(row[1])):
                continue

            discordIndex = self.values[0].index('_Discord')
            while(len(row) <= discordIndex):
                row.append('')

            row[discordIndex] = text
        
        body = {'values': self.values}

        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=RANGE_NAME,
            valueInputOption='RAW', body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

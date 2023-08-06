import os.path
import pickle
from pathlib import Path
from typing import List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from norma43utils.services.service import Service


class GoogleSpreadsheetService(Service):
    CREDENTIALS_FILE_PATH = f"{str(Path.home())}/.norma43togooglespreadsheet/google/"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    RANGE = "n43!A:F"

    service = None

    def __init__(self):
        self._retrieve_credentials_and_create_service()

    def write(self, data: List[List[str]], spreadsheet_id: str) -> None:

        if self.service is None:
            raise ValueError("GoogleSpreadsheetService not properly initialized")

        sheet = self.service.spreadsheets()
        resource = {"majorDimension": "ROWS", "values": data}

        sheet.values().append(
            spreadsheetId=spreadsheet_id, range=self.RANGE, body=resource, valueInputOption="USER_ENTERED"
        ).execute()

    def _retrieve_credentials_and_create_service(self):

        credentials = None

        Path(self.CREDENTIALS_FILE_PATH).mkdir(parents=True, exist_ok=True)
        token_pickle = f"{self.CREDENTIALS_FILE_PATH}token.pickle"

        if os.path.exists(token_pickle):
            with open(token_pickle, "rb") as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials_file_path = f"{self.CREDENTIALS_FILE_PATH}credentials.json"
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file_path, self.SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_pickle, "wb") as token:
                pickle.dump(credentials, token)

        self.service = build("sheets", "v4", credentials=credentials)

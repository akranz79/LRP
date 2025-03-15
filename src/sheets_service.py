from googleapiclient.discovery import build
from google.oauth2 import service_account

# Substitua pelo caminho correto do seu JSON de credenciais
SERVICE_ACCOUNT_FILE = "../config/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


# Configura a API do Google Sheets
def get_google_sheet(spreadsheet_id, sheet_name):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()

    return sheet.get("values", [])

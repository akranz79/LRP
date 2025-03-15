import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Caminho para o arquivo JSON da chave de serviço
SERVICE_ACCOUNT_FILE = "../config/credentials.json"

# ID da planilha (pegue da URL do Google Sheets)
SPREADSHEET_ID = "1YuS1YoQ74YsgNoGcBCmWVvIhEVhMZHWbz5R_zFgpKpE"


def verificar_acesso():
    try:
        # Definir escopo da API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

        # Autenticação
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(creds)

        # Acessar a planilha
        sheet = client.open_by_key(SPREADSHEET_ID)
        print(f"✅ Conexão bem-sucedida! Planilha '{sheet.title}' acessada.")

        # Listar abas da planilha
        worksheets = sheet.worksheets()
        print("📄 Abas disponíveis:")
        for ws in worksheets:
            print(f"- {ws.title}")

    except Exception as e:
        print(f"❌ Erro ao acessar a planilha: {e}")


# Executar teste
verificar_acesso()

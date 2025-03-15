import json
from config import PROCESSADOS_FILE

def carregar_processados():
    """Carrega os índices das linhas já processadas."""
    try:
        with open(PROCESSADOS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_processado(index):
    """Salva um novo índice de linha processada."""
    processados = carregar_processados()
    if index not in processados:
        processados.append(index)
        with open(PROCESSADOS_FILE, "w") as file:
            json.dump(processados, file)

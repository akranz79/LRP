import json
from datetime import datetime
from config import PROCESSADOS_FILE

def carregar_processados():
    """Carrega os índices das linhas já processadas"""
    try:
        with open(PROCESSADOS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_processado(index):
    """Salva uma nova linha processada"""
    processados = carregar_processados()
    processados.append(index)
    with open(PROCESSADOS_FILE, "w") as file:
        json.dump(processados, file)

def calcular_idade(data_nascimento):
    """Calcula a idade com base na data de nascimento"""
    try:
        nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        hoje = datetime.today()
        return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    except ValueError:
        return None



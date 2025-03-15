import json
from datetime import datetime
from sheets_service import get_google_sheet


def carregar_processados():
    """Carrega os índices das linhas já processadas."""
    try:
        with open("processados.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_processado(index):
    """Salva um novo índice de linha processado."""
    processados = carregar_processados()
    processados.append(index)
    with open("processados.json", "w") as file:
        json.dump(processados, file)


def carregar_config():
    """Carrega o arquivo de configuração contendo mapeamento de linguagens e descrições."""
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Erro ao carregar config.json. Certifique-se de que ele existe e está formatado corretamente.")
        return {"language_mapping": {}, "descricoes": {}}


CONFIG = carregar_config()
LANGUAGE_MAPPING = CONFIG.get("language_mapping", {})
DESCRICOES = CONFIG.get("descricoes", {})


def calcular_idade(data_nascimento):
    """Calcula a idade baseada na data de nascimento."""
    nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
    hoje = datetime.today()
    return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))


def calcular_pontuacoes(respostas):
    """Calcula as pontuações das linguagens do amor com base nas respostas."""
    scores = {chave: 0 for chave in DESCRICOES.keys()}  # Inicializa todas as linguagens com 0 pontos

    for i, resposta in enumerate(respostas):
        try:
            valor = int(resposta)
        except ValueError:
            continue

        chave_a = f"{chr(67 + i)}A"
        chave_b = f"{chr(67 + i)}B"

        linguagem_a = LANGUAGE_MAPPING.get(chave_a, None)
        linguagem_b = LANGUAGE_MAPPING.get(chave_b, None)

        if valor == 1 and linguagem_a:
            scores[linguagem_a] += 3
        elif valor == 2 and linguagem_a:
            scores[linguagem_a] += 2
        elif valor == 3 and linguagem_a and linguagem_b:
            scores[linguagem_a] += 1
            scores[linguagem_b] += 1
        elif valor == 4 and linguagem_b:
            scores[linguagem_b] += 2
        elif valor == 5 and linguagem_b:
            scores[linguagem_b] += 3

    return scores


def processar_proxima_linha(spreadsheet_id, sheet_name):
    """Processa a próxima linha não lida da planilha."""
    data = get_google_sheet(spreadsheet_id, sheet_name)
    processados = carregar_processados()

    for index, linha in enumerate(data[1:], start=1):  # Ignora cabeçalhos
        if index not in processados:
            data_preenchimento = linha[0]
            email = linha[1]
            nome = linha[12]
            data_nascimento = linha[13]
            idade = calcular_idade(data_nascimento)
            respostas = linha[2:12]

            scores = calcular_pontuacoes(respostas)
            total_pontos = sum(scores.values())

            if total_pontos == 0:
                print("Erro: Total de pontos é zero, possível erro nos dados.")
                return None

            resultado_ordenado = sorted(scores.items(), key=lambda x: x[1], reverse=True)

            linguagem_predominante = resultado_ordenado[0][0].strip()  # Remove espaços extras

            descricao = DESCRICOES.get(linguagem_predominante, "Descrição não disponível.")

            resultado = {
                "Nome": nome,
                "Idade": idade,
                "Email": email,
                "Data": data_preenchimento,
                "Linguagem Predominante": linguagem_predominante,
                "Descricao": descricao,  # Certifique-se de que esta chave existe
                "Linguagens": [(linguagem, (pontos / total_pontos) * 100) for linguagem, pontos in resultado_ordenado]
            }

            print(f"DEBUG: Linguagem Predominante: {linguagem_predominante} - Descrição: {descricao}")  # Depuração

            salvar_processado(index)
            return resultado

    print("Nenhuma nova linha para processar.")
    return None

import time
import subprocess

# Configuração do intervalo de tempo em segundos (exemplo: a cada 10 minutos)
INTERVALO_TEMPO = 180  # 600 segundos = 10 minutos

# Caminho para o script principal
SCRIPT_MAIN = "main.py"

def executar_script():
    """Executa o script main.py"""
    print("[LOG] Executando main.py...")
    subprocess.run(["python", SCRIPT_MAIN])
    print("[LOG] Execução concluída. Aguardando próximo ciclo...")

if __name__ == "__main__":
    while True:
        executar_script()
        print(f"[LOG] Aguardando {INTERVALO_TEMPO / 60} minutos para a próxima execução...")
        time.sleep(INTERVALO_TEMPO)

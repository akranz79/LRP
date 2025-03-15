from config import SPREADSHEET_ID, SHEET_NAME
from processor import processar_proxima_linha
from pdf_generator import salvar_resultado_em_pdf, enviar_email_com_pdf


def main():
    resultado = processar_proxima_linha(SPREADSHEET_ID, SHEET_NAME)
    if resultado:
        print("Resultado processado:", resultado)  # Depuração para ver se a descrição está presente
        nome_arquivo = f"resultado_{resultado['Nome'].replace(' ', '_')}.pdf"
        caminho_pdf = salvar_resultado_em_pdf(resultado, nome_arquivo)

        print(f"PDF gerado com sucesso: {caminho_pdf}")

        # Enviar o e-mail com o PDF
        print("[LOG] Chamando função de envio de e-mail...")
        enviar_email_com_pdf(resultado["Email"], caminho_pdf)
    else:
        print("Nenhum novo resultado processado.")


if __name__ == "__main__":
    main()


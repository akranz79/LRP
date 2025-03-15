from fpdf import FPDF
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def salvar_resultado_em_pdf(resultado, nome_arquivo):
    """Gera e salva um PDF com o resultado do teste."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "RESULTADO TESTE", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Nome: {resultado['Nome']}", ln=True)
    pdf.cell(200, 10, f"Idade: {resultado['Idade']}", ln=True)
    pdf.cell(200, 10, f"Email: {resultado['Email']}", ln=True)
    pdf.cell(200, 10, f"Data: {resultado['Data']}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "Linguagens Ordenadas (%)", ln=True)
    pdf.set_font("Arial", size=12)
    for linguagem, porcentagem in resultado["Linguagens"]:
        pdf.cell(200, 10, f"{linguagem}: {porcentagem:.2f}%", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(200, 10, "Descrição Linguagem Predominante", ln=True)
    pdf.set_font("Arial", size=12)
    descricao = resultado.get("Descricao", "Descrição não disponível.")
    pdf.multi_cell(0, 10, descricao)

    pdf_dir = os.path.join(os.path.dirname(__file__), "../pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    caminho_pdf = os.path.join(pdf_dir, nome_arquivo)
    pdf.output(caminho_pdf)
    print(f"PDF salvo: {caminho_pdf}")

    return caminho_pdf


def enviar_email_com_pdf(destinatario, caminho_pdf):
    """Envia o PDF gerado para o e-mail do candidato com logs detalhados."""
    remetente = "gs.223.talent@gmail.com"  # Altere para seu e-mail
    senha = "dzkp qmdv hgdm jxtx"  # Altere para sua senha ou senha de aplicativo
    assunto = "Resultado do Teste de Linguagens do Amor"
    corpo_email = "Segue em anexo o resultado do seu teste."

    try:
        print("[LOG] Iniciando envio de e-mail...")
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo_email, 'plain'))

        with open(caminho_pdf, "rb") as anexo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(anexo.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(caminho_pdf)}')
            msg.attach(part)

        print("[LOG] Conectando ao servidor SMTP...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            print("[LOG] Autenticando no servidor...")
            server.login(remetente, senha)
            print("[LOG] Enviando e-mail...")
            server.sendmail(remetente, destinatario, msg.as_string())

        print(f"[LOG] E-mail enviado com sucesso para {destinatario}")
    except Exception as e:
        print(f"[ERRO] Falha no envio de e-mail: {e}")

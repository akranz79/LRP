from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from config import DESCRICOES

def salvar_resultado_em_pdf(resultado, nome_arquivo="resultado_teste.pdf"):
    """Gera e salva um PDF com o resultado do teste de Linguagens do Amor"""

    if not resultado:
        print("Nenhum resultado disponível para salvar.")
        return

    nome = resultado["Nome"]
    idade = resultado["Idade"]
    linguagem_predominante, _ = resultado["Resultado"][0]

    descricao = DESCRICOES.get(linguagem_predominante, "Sem descrição disponível.")

    pdf = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, altura - 80, "📌 Resultado do Teste")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, altura - 120, f"👤 Nome: {nome}")
    pdf.drawString(100, altura - 140, f"🎂 Idade: {idade} anos")

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, altura - 180, f"💖 Linguagem do Amor Predominante: {linguagem_predominante}")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(100, altura - 200, f"📜 Descrição: {descricao}")

    pdf.save()
    print(f"PDF salvo como {nome_arquivo}")

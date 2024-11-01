import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import time

# ativar emails 
def enviar_email(destinatario, assunto, mensagem):
    # Configuração do servidor SMTP (usando Gmail como exemplo)
    servidor = 'smtp.gmail.com'
    porta = 587
    remetente = 'rodriguinhoabel77@gmail.com'
    senha = ''

    # Criando o e-mail
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    # Conectando ao servidor e enviando o e-mail
    try:
        server = smtplib.SMTP(servidor, porta)
        server.starttls()  # Iniciando conexão segura
        server.login(remetente, senha)
        texto = msg.as_string()
        server.sendmail(remetente, destinatario, texto)
        print(f"E-mail enviado para {destinatario}")
        server.quit()
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Função que verifica se faltam 30 dias para o evento
def verificar_evento(data_evento, destinatario):
    hoje = datetime.now().date()
    delta = data_evento - hoje

    if delta == timedelta(days=30):
        assunto = "Lembrete: Faltam 30 dias para o seu evento!"
        mensagem = f"Olá, faltam exatamente 30 dias para o evento marcado para {data_evento}."
        enviar_email(destinatario, assunto, mensagem)

# Função para agendar a verificação diária
def agendar_verificacao(data_evento_str, destinatario):
    # Converter a string de data para um objeto datetime
    data_evento = datetime.strptime(data_evento_str, "%Y-%m-%d").date()

    # Usar a biblioteca schedule para rodar a cada dia
    schedule.every().day.at("16:30").do(verificar_evento, data_evento, destinatario)


    print("Verificação diária agendada. O programa irá rodar todo dia às 16:30.")

    # Loop para rodar o agendamento de verificação
    while True:
        schedule.run_pending()
        time.sleep(60)  # Checa a cada minuto

# aq vc altera a data do evento e coloca a pessoa que vai receber o email.
data_evento = "2024-11-28"  
email_destinatario = "rodriguinhoabel77@gmail.com"

# aqui começa a verificação diaria
agendar_verificacao(data_evento, email_destinatario) 
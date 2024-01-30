from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import datetime
import shutil
import time
import os

def organize_workspace(workspace_path):
    file_extensions = set()
    nome_arquivo = 'organizador'

    for filename in os.listdir(workspace_path):
        if os.path.isfile(os.path.join(workspace_path, filename)):
            file_extension = filename.split(".")[-1].lower()
            file_extensions.add(file_extension)
    list_infos = []
    # Criar pastas para cada extensão e mover os arquivos correspondentes
    for extension in file_extensions:
        folder_name = extension.capitalize() + " Files"
        folder_path = os.path.join(workspace_path, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        for filename in os.listdir(workspace_path):
            if os.path.isfile(os.path.join(workspace_path, filename)):
                file_extension = filename.split(".")[-1].lower()
                if file_extension == extension:
                    old_file_path = os.path.join(workspace_path, filename)
                    new_file_path = os.path.join(folder_path, filename)
                    if filename != nome_arquivo:
                        shutil.move(old_file_path, new_file_path)
                        list_infos.append(f"Arquivo {filename} movido para {folder_name}")
                        print(f"Arquivo {filename} movido para {folder_name}")
                        
    load_dotenv()
    email = os.getenv("EMAIL")
    senha = os.getenv("SENHA")

    msg = EmailMessage()
    msg['Sebject'] = "ENVIO DE E-MAIL COM SMTPLIB"
    msg['To'] = email
    msg['From'] = os.getenv("DEST")

    conteudo_lista = '\n'.join(list_infos)
    msg.set_content(conteudo_lista)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, senha)
        smtp.send_message(msg)
    print('Email enviado com sucesso!')      
                 
def esperar_horario_especifico(horario_especifico, caminho):
    while True:
        agora = datetime.datetime.now().time()
        print(agora)
        if agora >= horario_especifico:
            break
        else:
            tempo_espera = (datetime.datetime.combine(datetime.date.today(), horario_especifico) - datetime.datetime.now()).total_seconds()
            time.sleep(max(1, tempo_espera))
            
    organize_workspace(r''+caminho)
    
caminho = input('Digite o caminho completo da pasta aqui: ')
horario_desejado = datetime.time(18, 26, 0) #aqui você coloca a hora, minuto, segundo que deseja executar
print(horario_desejado)
esperar_horario_especifico(horario_desejado)
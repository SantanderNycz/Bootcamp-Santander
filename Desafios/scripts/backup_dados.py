"""
Script para realizar backup dos dados do sistema bancário
"""
import os
import json
import datetime
import shutil
import zipfile

# Constantes
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"
ARQUIVO_TRANSACOES = "transacoes.json"
DIRETORIO_BACKUP = "backups"

def realizar_backup():
    """Realiza o backup dos dados do sistema"""
    # Verificar se os arquivos existem
    arquivos = [ARQUIVO_USUARIOS, ARQUIVO_CONTAS, ARQUIVO_TRANSACOES]
    arquivos_existentes = [arquivo for arquivo in arquivos if os.path.exists(arquivo)]
    
    if not arquivos_existentes:
        print("Nenhum arquivo de dados encontrado para backup.")
        return
    
    # Criar diretório de backup se não existir
    if not os.path.exists(DIRETORIO_BACKUP):
        os.makedirs(DIRETORIO_BACKUP)
    
    # Gerar nome do arquivo de backup com data e hora
    data_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_backup = f"backup_{data_hora}.zip"
    caminho_backup = os.path.join(DIRETORIO_BACKUP, nome_backup)
    
    # Criar arquivo ZIP com os dados
    with zipfile.ZipFile(caminho_backup, 'w') as zip_file:
        for arquivo in arquivos_existentes:
            zip_file.write(arquivo)
    
    print(f"Backup realizado com sucesso: {caminho_backup}")
    print(f"Arquivos incluídos: {', '.join(arquivos_existentes)}")

if __name__ == "__main__":
    realizar_backup()

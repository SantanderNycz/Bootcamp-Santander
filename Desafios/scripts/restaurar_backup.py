"""
Script para restaurar backup dos dados do sistema bancário
"""
import os
import zipfile
import glob

# Constantes
DIRETORIO_BACKUP = "backups"

def listar_backups():
    """Lista todos os backups disponíveis"""
    if not os.path.exists(DIRETORIO_BACKUP):
        print("Diretório de backups não encontrado.")
        return []
    
    backups = glob.glob(os.path.join(DIRETORIO_BACKUP, "backup_*.zip"))
    backups.sort(reverse=True)  # Ordenar do mais recente para o mais antigo
    
    return backups

def restaurar_backup(caminho_backup):
    """Restaura um backup específico"""
    if not os.path.exists(caminho_backup):
        print(f"Arquivo de backup não encontrado: {caminho_backup}")
        return False
    
    try:
        with zipfile.ZipFile(caminho_backup, 'r') as zip_file:
            # Extrair todos os arquivos
            zip_file.extractall()
        
        print(f"Backup restaurado com sucesso: {caminho_backup}")
        print(f"Arquivos restaurados: {', '.join(zipfile.ZipFile(caminho_backup, 'r').namelist())}")
        return True
    except Exception as e:
        print(f"Erro ao restaurar backup: {e}")
        return False

def main():
    """Função principal do script"""
    print("===== RESTAURAÇÃO DE BACKUP =====")
    
    backups = listar_backups()
    
    if not backups:
        print("Nenhum backup disponível para restauração.")
        return
    
    print("\nBackups disponíveis:")
    for i, backup in enumerate(backups):
        nome_arquivo = os.path.basename(backup)
        print(f"[{i+1}] {nome_arquivo}")
    
    try:
        escolha = int(input("\nEscolha o número do backup para restaurar (0 para cancelar): "))
        
        if escolha == 0:
            print("Operação cancelada.")
            return
        
        if 1 <= escolha <= len(backups):
            backup_escolhido = backups[escolha-1]
            
            confirmacao = input(f"Tem certeza que deseja restaurar o backup {os.path.basename(backup_escolhido)}? (s/n): ")
            
            if confirmacao.lower() == 's':
                restaurar_backup(backup_escolhido)
            else:
                print("Operação cancelada.")
        else:
            print("Opção inválida.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

if __name__ == "__main__":
    main()

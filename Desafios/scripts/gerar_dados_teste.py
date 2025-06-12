"""
Script para gerar dados de teste para o sistema bancário
"""
import os
import sys
import json
import hashlib
import datetime

# Adicionar o diretório pai ao path para importar o módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constantes
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"
ARQUIVO_TRANSACOES = "transacoes.json"

def gerar_hash_senha(senha):
    """Gera um hash da senha para armazenamento seguro"""
    return hashlib.sha256(senha.encode()).hexdigest()

def gerar_dados_teste():
    """Gera dados de teste para o sistema bancário"""
    # Dados de usuários
    usuarios = {
        "12345678900": {
            "cpf": "12345678900",
            "nome": "João da Silva",
            "data_nascimento": "01/01/1990",
            "endereco": "Rua A, 123",
            "senha_hash": gerar_hash_senha("Senha123")
        },
        "98765432100": {
            "cpf": "98765432100",
            "nome": "Maria Oliveira",
            "data_nascimento": "15/05/1985",
            "endereco": "Av. B, 456",
            "senha_hash": gerar_hash_senha("Senha456")
        }
    }
    
    # Dados de contas
    contas = {
        "1": {
            "numero": 1,
            "agencia": "0001",
            "cpf_usuario": "12345678900",
            "saldo": 1500.0,
            "limite": 500.0,
            "saques_hoje": 0,
            "data_ultimo_saque": None
        },
        "2": {
            "numero": 2,
            "agencia": "0001",
            "cpf_usuario": "98765432100",
            "saldo": 2500.0,
            "limite": 1000.0,
            "saques_hoje": 0,
            "data_ultimo_saque": None
        }
    }
    
    # Dados de transações
    data_base = datetime.datetime.now() - datetime.timedelta(days=5)
    
    transacoes = [
        {
            "id": hashlib.md5(f"{data_base.isoformat()}-1".encode()).hexdigest(),
            "tipo": "deposito",
            "valor": 1000.0,
            "conta_origem": 1,
            "conta_destino": None,
            "descricao": "Depósito inicial",
            "data_hora": (data_base + datetime.timedelta(hours=1)).isoformat()
        },
        {
            "id": hashlib.md5(f"{data_base.isoformat()}-2".encode()).hexdigest(),
            "tipo": "deposito",
            "valor": 2000.0,
            "conta_origem": 2,
            "conta_destino": None,
            "descricao": "Depósito inicial",
            "data_hora": (data_base + datetime.timedelta(hours=2)).isoformat()
        },
        {
            "id": hashlib.md5(f"{data_base.isoformat()}-3".encode()).hexdigest(),
            "tipo": "saque",
            "valor": 200.0,
            "conta_origem": 1,
            "conta_destino": None,
            "descricao": "Saque em conta",
            "data_hora": (data_base + datetime.timedelta(days=1)).isoformat()
        },
        {
            "id": hashlib.md5(f"{data_base.isoformat()}-4".encode()).hexdigest(),
            "tipo": "transferencia",
            "valor": 500.0,
            "conta_origem": 2,
            "conta_destino": 1,
            "descricao": "Transferência entre contas",
            "data_hora": (data_base + datetime.timedelta(days=2)).isoformat()
        }
    ]
    
    # Salvar os dados em arquivos JSON
    with open(ARQUIVO_USUARIOS, "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)
    
    with open(ARQUIVO_CONTAS, "w") as arquivo:
        json.dump(contas, arquivo, indent=4)
    
    with open(ARQUIVO_TRANSACOES, "w") as arquivo:
        json.dump(transacoes, arquivo, indent=4)
    
    print("Dados de teste gerados com sucesso!")
    print(f"Usuários: {len(usuarios)}")
    print(f"Contas: {len(contas)}")
    print(f"Transações: {len(transacoes)}")
    print("\nCredenciais de acesso:")
    print("CPF: 12345678900 | Senha: Senha123")
    print("CPF: 98765432100 | Senha: Senha456")

if __name__ == "__main__":
    gerar_dados_teste()

"""
Script para gerar relatórios sobre as contas do sistema bancário
"""
import os
import json
import datetime
import sys

# Adicionar o diretório pai ao path para importar o módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Constantes
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_CONTAS = "contas.json"
ARQUIVO_TRANSACOES = "transacoes.json"

def carregar_dados():
    """Carrega os dados do sistema a partir dos arquivos JSON"""
    usuarios = {}
    contas = {}
    transacoes = []
    
    # Carregar usuários
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "r") as arquivo:
            usuarios = json.load(arquivo)
    
    # Carregar contas
    if os.path.exists(ARQUIVO_CONTAS):
        with open(ARQUIVO_CONTAS, "r") as arquivo:
            contas = json.load(arquivo)
    
    # Carregar transações
    if os.path.exists(ARQUIVO_TRANSACOES):
        with open(ARQUIVO_TRANSACOES, "r") as arquivo:
            transacoes = json.load(arquivo)
    
    return usuarios, contas, transacoes

def relatorio_saldo_total():
    """Gera um relatório com o saldo total de todas as contas"""
    _, contas, _ = carregar_dados()
    
    if not contas:
        print("Nenhuma conta encontrada.")
        return
    
    saldo_total = sum(float(conta["saldo"]) for conta in contas.values())
    qtd_contas = len(contas)
    
    print("===== RELATÓRIO DE SALDO TOTAL =====")
    print(f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Quantidade de contas: {qtd_contas}")
    print(f"Saldo total: R$ {saldo_total:.2f}")
    print(f"Saldo médio por conta: R$ {(saldo_total / qtd_contas if qtd_contas > 0 else 0):.2f}")

def relatorio_transacoes_periodo():
    """Gera um relatório de transações por período"""
    _, _, transacoes = carregar_dados()
    
    if not transacoes:
        print("Nenhuma transação encontrada.")
        return
    
    print("===== RELATÓRIO DE TRANSAÇÕES POR PERÍODO =====")
    
    # Solicitar período
    data_inicio_str = input("Data inicial (DD/MM/AAAA): ")
    data_fim_str = input("Data final (DD/MM/AAAA): ")
    
    try:
        data_inicio = datetime.datetime.strptime(data_inicio_str, "%d/%m/%Y")
        data_fim = datetime.datetime.strptime(data_fim_str, "%d/%m/%Y")
        data_fim = data_fim.replace(hour=23, minute=59, second=59)  # Fim do dia
    except ValueError:
        print("Formato de data inválido.")
        return
    
    # Filtrar transações no período
    transacoes_periodo = []
    for t in transacoes:
        data_transacao = datetime.datetime.fromisoformat(t["data_hora"])
        if data_inicio <= data_transacao <= data_fim:
            transacoes_periodo.append(t)
    
    if not transacoes_periodo:
        print(f"Nenhuma transação encontrada no período de {data_inicio_str} a {data_fim_str}.")
        return
    
    # Calcular estatísticas
    qtd_depositos = sum(1 for t in transacoes_periodo if t["tipo"] == "deposito")
    qtd_saques = sum(1 for t in transacoes_periodo if t["tipo"] == "saque")
    qtd_transferencias = sum(1 for t in transacoes_periodo if t["tipo"] == "transferencia")
    
    valor_depositos = sum(t["valor"] for t in transacoes_periodo if t["tipo"] == "deposito")
    valor_saques = sum(t["valor"] for t in transacoes_periodo if t["tipo"] == "saque")
    valor_transferencias = sum(t["valor"] for t in transacoes_periodo if t["tipo"] == "transferencia")
    
    # Exibir relatório
    print(f"\nPeríodo: {data_inicio_str} a {data_fim_str}")
    print(f"Total de transações: {len(transacoes_periodo)}")
    print("\nQuantidade por tipo:")
    print(f"- Depósitos: {qtd_depositos}")
    print(f"- Saques: {qtd_saques}")
    print(f"- Transferências: {qtd_transferencias}")
    print("\nValor total por tipo:")
    print(f"- Depósitos: R$ {valor_depositos:.2f}")
    print(f"- Saques: R$ {valor_saques:.2f}")
    print(f"- Transferências: R$ {valor_transferencias:.2f}")

def relatorio_contas_por_usuario():
    """Gera um relatório de contas por usuário"""
    usuarios, contas, _ = carregar_dados()
    
    if not usuarios or not contas:
        print("Nenhum usuário ou conta encontrada.")
        return
    
    print("===== RELATÓRIO DE CONTAS POR USUÁRIO =====")
    print(f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Mapear contas por CPF do usuário
    contas_por_usuario = {}
    for num_conta, conta in contas.items():
        cpf = conta["cpf_usuario"]
        if cpf not in contas_por_usuario:
            contas_por_usuario[cpf] = []
        contas_por_usuario[cpf].append(conta)
    
    # Exibir relatório
    for cpf, contas_usuario in contas_por_usuario.items():
        if cpf in usuarios:
            usuario = usuarios[cpf]
            print(f"\nUsuário: {usuario['nome']} (CPF: {cpf})")
            print(f"Quantidade de contas: {len(contas_usuario)}")
            
            for conta in contas_usuario:
                print(f"  - Conta: {conta['numero']} | Agência: {conta['agencia']} | Saldo: R$ {conta['saldo']:.2f}")

def menu_relatorios():
    """Exibe o menu de relatórios"""
    print("\n===== RELATÓRIOS =====")
    print("[1] Saldo total de todas as contas")
    print("[2] Transações por período")
    print("[3] Contas por usuário")
    print("[0] Voltar")
    return input("\n=> ")

def main():
    """Função principal do script"""
    while True:
        opcao = menu_relatorios()
        
        if opcao == "1":
            relatorio_saldo_total()
        elif opcao == "2":
            relatorio_transacoes_periodo()
        elif opcao == "3":
            relatorio_contas_por_usuario()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()

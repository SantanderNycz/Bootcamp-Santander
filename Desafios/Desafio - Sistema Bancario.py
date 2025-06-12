"""
Sistema Bancário Simplificado
Desenvolvido para aprendizado de programação Python - Nível Júnior Entry Level
"""
import os
import time
from datetime import datetime

# Variáveis globais para armazenar os dados do sistema
usuarios = {}  # Dicionário para armazenar os usuários {cpf: {"nome": nome, "senha": senha}}
contas = {}    # Dicionário para armazenar as contas {numero: {"saldo": saldo, "limite": limite, "cpf": cpf}}
transacoes = []  # Lista para armazenar as transações

# Constantes do sistema
LIMITE_SAQUES = 3
LIMITE_PADRAO = 500.0
AGENCIA = "0001"

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def formatar_cpf(cpf):
    """Formata um CPF para exibição (ex: 123.456.789-00)"""
    # Remove caracteres não numéricos
    cpf_limpo = ''.join(c for c in cpf if c.isdigit())
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        return cpf
    
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

def validar_cpf_simples(cpf):
    """Faz uma validação simples de CPF (apenas verifica se tem 11 dígitos)"""
    cpf_limpo = ''.join(c for c in cpf if c.isdigit())
    return len(cpf_limpo) == 11

def criar_usuario():
    """Cria um novo usuário no sistema"""
    limpar_tela()
    print("===== CADASTRO DE NOVO USUÁRIO =====")
    
    cpf = input("CPF (apenas números): ")
    
    # Validação simples do CPF
    if not validar_cpf_simples(cpf):
        print("CPF inválido! O CPF deve ter 11 dígitos.")
        return False
    
    # Verificar se o CPF já está cadastrado
    if cpf in usuarios:
        print("CPF já cadastrado no sistema!")
        return False
    
    nome = input("Nome completo: ")
    senha = input("Senha: ")
    
    # Validação simples da senha
    if len(senha) < 4:
        print("A senha deve ter pelo menos 4 caracteres!")
        return False
    
    # Armazenar o usuário
    usuarios[cpf] = {
        "nome": nome,
        "senha": senha,
        "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    
    print(f"\nUsuário {nome} cadastrado com sucesso!")
    return True

def criar_conta():
    """Cria uma nova conta para um usuário existente"""
    limpar_tela()
    print("===== CRIAÇÃO DE NOVA CONTA =====")
    
    cpf = input("Informe o CPF do titular: ")
    
    # Verificar se o usuário existe
    if cpf not in usuarios:
        print("Usuário não encontrado! Cadastre-se primeiro.")
        return False
    
    # Gerar número da conta (simples, apenas para exemplo)
    numero_conta = str(len(contas) + 1).zfill(4)  # Preenche com zeros à esquerda
    
    # Criar a conta
    contas[numero_conta] = {
        "saldo": 0.0,
        "limite": LIMITE_PADRAO,
        "cpf": cpf,
        "saques_hoje": 0,
        "data_ultimo_saque": None
    }
    
    print(f"\nConta criada com sucesso!")
    print(f"Número da conta: {numero_conta}")
    print(f"Agência: {AGENCIA}")
    return True

def autenticar_usuario():
    """Autentica um usuário no sistema"""
    limpar_tela()
    print("===== LOGIN =====")
    
    cpf = input("CPF: ")
    senha = input("Senha: ")
    
    if cpf in usuarios and usuarios[cpf]["senha"] == senha:
        return cpf
    
    print("CPF ou senha incorretos!")
    return None

def encontrar_conta_por_cpf(cpf):
    """Encontra a conta de um usuário pelo CPF"""
    for numero, conta in contas.items():
        if conta["cpf"] == cpf:
            return numero
    return None

def depositar(numero_conta):
    """Realiza um depósito em uma conta"""
    limpar_tela()
    print("===== DEPÓSITO =====")
    
    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        
        if valor <= 0:
            print("Valor inválido! O valor deve ser positivo.")
            return False
        
        # Atualizar o saldo
        contas[numero_conta]["saldo"] += valor
        
        # Registrar a transação
        transacoes.append({
            "tipo": "deposito",
            "valor": valor,
            "conta": numero_conta,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True
    except ValueError:
        print("Valor inválido! Digite um número válido.")
        return False

def sacar(numero_conta):
    """Realiza um saque em uma conta"""
    limpar_tela()
    print("===== SAQUE =====")
    
    # Verificar se é um novo dia para resetar o contador de saques
    hoje = datetime.now().strftime("%d/%m/%Y")
    if contas[numero_conta]["data_ultimo_saque"] != hoje:
        contas[numero_conta]["saques_hoje"] = 0
        contas[numero_conta]["data_ultimo_saque"] = hoje
    
    # Verificar se já atingiu o limite de saques
    if contas[numero_conta]["saques_hoje"] >= LIMITE_SAQUES:
        print(f"Limite diário de {LIMITE_SAQUES} saques atingido!")
        return False
    
    try:
        valor = float(input("Informe o valor do saque: R$ "))
        
        # Validações
        if valor <= 0:
            print("Valor inválido! O valor deve ser positivo.")
            return False
        
        if valor > contas[numero_conta]["saldo"]:
            print("Saldo insuficiente para realizar o saque!")
            return False
        
        if valor > contas[numero_conta]["limite"]:
            print(f"Valor excede o limite de saque (R$ {contas[numero_conta]['limite']:.2f})!")
            return False
        
        # Realizar o saque
        contas[numero_conta]["saldo"] -= valor
        contas[numero_conta]["saques_hoje"] += 1
        
        # Registrar a transação
        transacoes.append({
            "tipo": "saque",
            "valor": valor,
            "conta": numero_conta,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
        return True
    except ValueError:
        print("Valor inválido! Digite um número válido.")
        return False

def transferir(numero_conta_origem):
    """Realiza uma transferência entre contas"""
    limpar_tela()
    print("===== TRANSFERÊNCIA =====")
    
    numero_conta_destino = input("Informe o número da conta de destino: ")
    
    # Verificar se a conta de destino existe
    if numero_conta_destino not in contas:
        print("Conta de destino não encontrada!")
        return False
    
    # Verificar se não é a mesma conta
    if numero_conta_origem == numero_conta_destino:
        print("Não é possível transferir para a própria conta!")
        return False
    
    try:
        valor = float(input("Informe o valor da transferência: R$ "))
        
        # Validações
        if valor <= 0:
            print("Valor inválido! O valor deve ser positivo.")
            return False
        
        if valor > contas[numero_conta_origem]["saldo"]:
            print("Saldo insuficiente para realizar a transferência!")
            return False
        
        # Realizar a transferência
        contas[numero_conta_origem]["saldo"] -= valor
        contas[numero_conta_destino]["saldo"] += valor
        
        # Registrar a transação
        transacoes.append({
            "tipo": "transferencia",
            "valor": valor,
            "conta_origem": numero_conta_origem,
            "conta_destino": numero_conta_destino,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
        
        print(f"Transferência de R$ {valor:.2f} realizada com sucesso!")
        return True
    except ValueError:
        print("Valor inválido! Digite um número válido.")
        return False

def exibir_extrato(numero_conta):
    """Exibe o extrato de uma conta"""
    limpar_tela()
    print("===== EXTRATO =====")
    print(f"Conta: {numero_conta} | Agência: {AGENCIA}")
    print(f"Titular: {usuarios[contas[numero_conta]['cpf']]['nome']}")
    print("\n--- Movimentações ---")
    
    # Filtrar transações da conta
    transacoes_conta = []
    for t in transacoes:
        if t["tipo"] == "deposito" and t["conta"] == numero_conta:
            transacoes_conta.append(t)
        elif t["tipo"] == "saque" and t["conta"] == numero_conta:
            transacoes_conta.append(t)
        elif t["tipo"] == "transferencia" and (t["conta_origem"] == numero_conta or t["conta_destino"] == numero_conta):
            transacoes_conta.append(t)
    
    if not transacoes_conta:
        print("Não foram realizadas movimentações.")
    else:
        for t in transacoes_conta:
            if t["tipo"] == "deposito":
                print(f"{t['data']} - Depósito: R$ {t['valor']:.2f}")
            elif t["tipo"] == "saque":
                print(f"{t['data']} - Saque: R$ {t['valor']:.2f}")
            elif t["tipo"] == "transferencia":
                if t["conta_origem"] == numero_conta:
                    print(f"{t['data']} - Transferência enviada: R$ {t['valor']:.2f} para conta {t['conta_destino']}")
                else:
                    print(f"{t['data']} - Transferência recebida: R$ {t['valor']:.2f} da conta {t['conta_origem']}")
    
    print(f"\nSaldo atual: R$ {contas[numero_conta]['saldo']:.2f}")
    print(f"Limite de saque: R$ {contas[numero_conta]['limite']:.2f}")
    print(f"Saques hoje: {contas[numero_conta]['saques_hoje']}/{LIMITE_SAQUES}")

def alterar_limite(numero_conta):
    """Altera o limite de saque de uma conta"""
    limpar_tela()
    print("===== ALTERAR LIMITE DE SAQUE =====")
    print(f"Limite atual: R$ {contas[numero_conta]['limite']:.2f}")
    
    try:
        novo_limite = float(input("Informe o novo limite de saque: R$ "))
        
        if novo_limite <= 0:
            print("Limite inválido! O valor deve ser positivo.")
            return False
        
        contas[numero_conta]["limite"] = novo_limite
        print(f"Limite alterado para R$ {novo_limite:.2f} com sucesso!")
        return True
    except ValueError:
        print("Valor inválido! Digite um número válido.")
        return False

def salvar_dados():
    """Salva os dados do sistema em arquivos de texto simples"""
    # Salvar usuários
    with open("usuarios.txt", "w") as arquivo:
        for cpf, dados in usuarios.items():
            linha = f"{cpf};{dados['nome']};{dados['senha']};{dados['data_cadastro']}\n"
            arquivo.write(linha)
    
    # Salvar contas
    with open("contas.txt", "w") as arquivo:
        for numero, dados in contas.items():
            linha = f"{numero};{dados['saldo']};{dados['limite']};{dados['cpf']};{dados['saques_hoje']};{dados['data_ultimo_saque']}\n"
            arquivo.write(linha)
    
    # Salvar transações
    with open("transacoes.txt", "w") as arquivo:
        for t in transacoes:
            if t["tipo"] == "transferencia":
                linha = f"{t['tipo']};{t['valor']};{t['conta_origem']};{t['conta_destino']};{t['data']}\n"
            else:
                linha = f"{t['tipo']};{t['valor']};{t['conta']};;{t['data']}\n"
            arquivo.write(linha)

def carregar_dados():
    """Carrega os dados do sistema a partir de arquivos de texto simples"""
    global usuarios, contas, transacoes
    
    # Carregar usuários
    if os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")
                if len(dados) >= 4:
                    cpf = dados[0]
                    usuarios[cpf] = {
                        "nome": dados[1],
                        "senha": dados[2],
                        "data_cadastro": dados[3]
                    }
    
    # Carregar contas
    if os.path.exists("contas.txt"):
        with open("contas.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")
                if len(dados) >= 6:
                    numero = dados[0]
                    contas[numero] = {
                        "saldo": float(dados[1]),
                        "limite": float(dados[2]),
                        "cpf": dados[3],
                        "saques_hoje": int(dados[4]),
                        "data_ultimo_saque": dados[5] if dados[5] != "None" else None
                    }
    
    # Carregar transações
    if os.path.exists("transacoes.txt"):
        with open("transacoes.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")
                if len(dados) >= 5:
                    tipo = dados[0]
                    valor = float(dados[1])
                    data = dados[4]
                    
                    if tipo == "transferencia":
                        transacoes.append({
                            "tipo": tipo,
                            "valor": valor,
                            "conta_origem": dados[2],
                            "conta_destino": dados[3],
                            "data": data
                        })
                    else:
                        transacoes.append({
                            "tipo": tipo,
                            "valor": valor,
                            "conta": dados[2],
                            "data": data
                        })

def criar_dados_exemplo():
    """Cria dados de exemplo para o sistema"""
    global usuarios, contas, transacoes
    
    # Criar usuários de exemplo
    usuarios = {
        "12345678900": {
            "nome": "João da Silva",
            "senha": "1234",
            "data_cadastro": "01/01/2023 10:00:00"
        },
        "98765432100": {
            "nome": "Maria Oliveira",
            "senha": "4321",
            "data_cadastro": "02/01/2023 11:00:00"
        }
    }
    
    # Criar contas de exemplo
    contas = {
        "0001": {
            "saldo": 1000.0,
            "limite": 500.0,
            "cpf": "12345678900",
            "saques_hoje": 0,
            "data_ultimo_saque": None
        },
        "0002": {
            "saldo": 2000.0,
            "limite": 1000.0,
            "cpf": "98765432100",
            "saques_hoje": 0,
            "data_ultimo_saque": None
        }
    }
    
    # Criar transações de exemplo
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    transacoes = [
        {
            "tipo": "deposito",
            "valor": 1000.0,
            "conta": "0001",
            "data": data_atual
        },
        {
            "tipo": "deposito",
            "valor": 2000.0,
            "conta": "0002",
            "data": data_atual
        },
        {
            "tipo": "transferencia",
            "valor": 500.0,
            "conta_origem": "0002",
            "conta_destino": "0001",
            "data": data_atual
        }
    ]
    
    print("Dados de exemplo criados com sucesso!")
    print("\nCredenciais de acesso:")
    print("CPF: 12345678900 | Senha: 1234 | Conta: 0001")
    print("CPF: 98765432100 | Senha: 4321 | Conta: 0002")

def menu_principal():
    """Exibe o menu principal do sistema"""
    limpar_tela()
    print("===== SISTEMA BANCÁRIO =====")
    print("[1] Criar usuário")
    print("[2] Criar conta")
    print("[3] Acessar conta")
    print("[4] Criar dados de exemplo")
    print("[0] Sair")
    return input("\n=> ")

def menu_conta(numero_conta):
    """Exibe o menu de operações da conta"""
    limpar_tela()
    print(f"===== CONTA: {numero_conta} =====")
    print(f"Titular: {usuarios[contas[numero_conta]['cpf']]['nome']}")
    print(f"Saldo: R$ {contas[numero_conta]['saldo']:.2f}")
    print("\n[d] Depositar")
    print("[s] Sacar")
    print("[t] Transferir")
    print("[e] Extrato")
    print("[l] Alterar limite de saque")
    print("[q] Sair")
    return input("\n=> ")

def main():
    """Função principal do sistema"""
    # Carregar dados salvos
    carregar_dados()
    
    while True:
        opcao = menu_principal()
        
        if opcao == "1":
            # Criar usuário
            if criar_usuario():
                salvar_dados()
            input("\nPressione Enter para continuar...")
        
        elif opcao == "2":
            # Criar conta
            if criar_conta():
                salvar_dados()
            input("\nPressione Enter para continuar...")
        
        elif opcao == "3":
            # Acessar conta
            cpf_usuario = autenticar_usuario()
            
            if cpf_usuario:
                numero_conta = encontrar_conta_por_cpf(cpf_usuario)
                
                if not numero_conta:
                    print("Você não possui uma conta. Crie uma conta primeiro.")
                    input("\nPressione Enter para continuar...")
                    continue
                
                # Menu da conta
                while True:
                    opcao_conta = menu_conta(numero_conta)
                    
                    if opcao_conta == "d":
                        if depositar(numero_conta):
                            salvar_dados()
                        input("\nPressione Enter para continuar...")
                    
                    elif opcao_conta == "s":
                        if sacar(numero_conta):
                            salvar_dados()
                        input("\nPressione Enter para continuar...")
                    
                    elif opcao_conta == "t":
                        if transferir(numero_conta):
                            salvar_dados()
                        input("\nPressione Enter para continuar...")
                    
                    elif opcao_conta == "e":
                        exibir_extrato(numero_conta)
                        input("\nPressione Enter para continuar...")
                    
                    elif opcao_conta == "l":
                        if alterar_limite(numero_conta):
                            salvar_dados()
                        input("\nPressione Enter para continuar...")
                    
                    elif opcao_conta == "q":
                        break
                    
                    else:
                        print("Opção inválida!")
                        time.sleep(1)
            else:
                input("\nPressione Enter para continuar...")
        
        elif opcao == "4":
            # Criar dados de exemplo
            criar_dados_exemplo()
            salvar_dados()
            input("\nPressione Enter para continuar...")
        
        elif opcao == "0":
            print("Obrigado por utilizar nosso sistema bancário!")
            break
        
        else:
            print("Opção inválida!")
            time.sleep(1)

if __name__ == "__main__":
    main()

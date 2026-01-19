import sys
from typing import List, Optional
from app.modelos.cliente import Cliente
from app.modelos.conta import Conta
from app.errors import SaldoInsuficienteError, ValorInvalidoError

class SistemaBancario:
    def __init__(self):
        self.contas: List[Conta] = []  

    def buscar_conta(self, numero: str) -> Optional[Conta]:
        for conta in self.contas:
            if conta.numero == numero:
                return conta
        return None

    def criar_conta(self):
        print("\n---Abertura de Conta ---")
        nome = input("Nome do Cliente: ")
        cpf = input("CPF: ")
        numero_conta = input("Número da nova conta (ex: 001): ")

        if self.buscar_conta(numero_conta):
            print("❌ Erro: Já existe uma conta com esse número!")
            return

        cliente = Cliente(nome, cpf)
        nova_conta = Conta(numero_conta, cliente)
        self.contas.append(nova_conta)
        print(f"✅ Conta {numero_conta} criada com sucesso para {nome}!")

    def realizar_deposito(self):
        print("\n--- 💰 Deposito ---")
        numero = input("Numero da conta: ")
        conta = self.buscar_conta(numero)

        if not conta:
            print("❌ Conta não encontrada.")
            return

        try:
            valor = float(input("Valor do deposito: R$ "))
            conta.depositar(valor)
            print(f"✅ Deposito realizado! Novo saldo: R$ {conta.saldo:.2f}")
        except ValorInvalidoError as e:
            print(f"❌ Erro: {e}")
        except ValueError:
            print("❌ Erro: Digite um número valido.")

    def realizar_saque(self):
        print("\n--- Saque ---")
        numero = input("Número da conta: ")
        conta = self.buscar_conta(numero)

        if not conta:
            print("❌ Conta não encontrada.")
            return

        try:
            valor = float(input("Valor do saque: R$ "))
            conta.sacar(valor)
            print(f"✅ Saque realizado! Novo saldo: R$ {conta.saldo:.2f}")
        except (SaldoInsuficienteError, ValorInvalidoError) as e:
            print(f"❌ Não foi possível sacar: {e}")
        except ValueError:
            print("❌ Erro: Digite um número válido.")

    def realizar_transferencia(self):
        print("\n--- 🔄 Transferência ---")
        origem_num = input("Conta de Origem: ")
        conta_origem = self.buscar_conta(origem_num)

        if not conta_origem:
            print("❌ Conta de origem não encontrada.")
            return

        destino_num = input("Conta de Destino: ")
        conta_destino = self.buscar_conta(destino_num)

        if not conta_destino:
            print("❌ Conta de destino não encontrada.")
            return
        
        if conta_origem == conta_destino:
             print("❌ Erro: Origem e destino são iguais.")
             return

        try:
            valor = float(input("Valor da transferência: R$ "))
            conta_origem.transferir(conta_destino, valor)
            print(f"✅ Transferência realizada com sucesso!")
        except (SaldoInsuficienteError, ValorInvalidoError) as e:
            print(f"❌ Falha na transferência: {e}")
        except ValueError:
             print("❌ Erro: Digite um número válido.")

    def exibir_extrato(self):
        print("\n---Extrato ---")
        numero = input("Número da conta: ")
        conta = self.buscar_conta(numero)

        if not conta:
            print("❌ Conta não encontrada.")
            return

        print(f"\nExtrato de {conta.titular.nome} (Conta: {conta.numero})")
        print("-" * 40)
        for log in conta.historico:
            print(f"{log['data']} | {log['tipo']:<20} | R$ {log['valor']:>10.2f}")
        print("-" * 40)
        print(f"Saldo Atual: R$ {conta.saldo:.2f}")

    def menu(self):
        while True:
            print("\n" + "="*30)
            print("  BANCO - MENU   ")
            print("="*30)
            print("1. Nova Conta")
            print("2. Depositar")
            print("3. Sacar")
            print("4. Transferir")
            print("5. Extrato")
            print("0. Sair")
            
            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                self.criar_conta()
            elif opcao == "2":
                self.realizar_deposito()
            elif opcao == "3":
                self.realizar_saque()
            elif opcao == "4":
                self.realizar_transferencia()
            elif opcao == "5":
                self.exibir_extrato()
            elif opcao == "0":
                print("Encerrando sistema... Até logo!")
                sys.exit()
            else:
                print("Opção invalida!")

if __name__ == "__main__":
    app = SistemaBancario()
    app.menu()
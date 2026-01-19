from datetime import datetime
from typing import List, Dict
from app.errors import SaldoInsuficienteError, ValorInvalidoError
from app.modelos.cliente import Cliente

class Conta:
    def __init__(self, numero: str, titular: Cliente):
        self.numero = numero
        self.titular = titular
        self.__saldo = 0.0 
        self.__historico: List[Dict] = [] 

    @property
    def saldo(self) -> float:
        return self.__saldo

    @property
    def historico(self) -> List[Dict]:
        return self.__historico

    def __registrar_operacao(self, tipo: str, valor: float):
        registro = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tipo": tipo,
            "valor": valor,
            "saldo_apos": self.__saldo
        }
        self.__historico.append(registro)

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValorInvalidoError("O valor do deposito deve ser positivo")
        
        self.__saldo += valor
        self.__registrar_operacao("Deposito", valor)

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo")
        
        if valor > self.__saldo:
            raise SaldoInsuficienteError(f"Saldo insuficiente. Disponivel: {self.__saldo}")
        
        self.__saldo -= valor
        self.__registrar_operacao("Saque", -valor)

    def transferir(self, conta_destino: 'Conta', valor: float):
        #Tentando sacar
        self.sacar(valor) 
        
        try:
            #Tentando depositar
            conta_destino.depositar(valor)
            
            # Ajusstando historico
            self.__historico.pop() 
            conta_destino._Conta__historico.pop()
            
            self.__registrar_operacao(f"Transferência enviada para {conta_destino.titular.nome}", -valor)
            conta_destino.__registrar_operacao(f"Transferência recebida de {self.titular.nome}", valor)
            
        except Exception as e:
            self.__saldo += valor 
            raise e
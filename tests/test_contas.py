import pytest
from app.modelos.cliente import Cliente
from app.modelos.conta import Conta
from app.errors import SaldoInsuficienteError, ValorInvalidoError

@pytest.fixture
def cliente_teste():
    return Cliente("Tester", "123.456.789-00")

@pytest.fixture
def conta_teste(cliente_teste):
    return Conta("001", cliente_teste)

@pytest.fixture
def conta_destino():
    cliente = Cliente("Destino", "000.000.000-00")
    return Conta("002", cliente)

class TestConta:
    
    def test_saldo_inicial_deve_ser_zero(self, conta_teste):
        assert conta_teste.saldo == 0

    def test_depositar_valor_positivo_deve_aumentar_saldo(self, conta_teste):
        conta_teste.depositar(100)
        assert conta_teste.saldo == 100
        # Verifica se registrou no historico
        assert len(conta_teste.historico) == 1
        assert conta_teste.historico[0]["tipo"] == "Depósito"

    def test_depositar_valor_negativo_deve_lancar_erro(self, conta_teste):
        with pytest.raises(ValorInvalidoError):
            conta_teste.depositar(-50)
        assert conta_teste.saldo == 0

    def test_sacar_valor_disponivel_deve_diminuir_saldo(self, conta_teste):
        conta_teste.depositar(100)
        conta_teste.sacar(30)
        assert conta_teste.saldo == 70
        assert conta_teste.historico[-1]["tipo"] == "Saque"

    def test_sacar_valor_indisponivel_deve_lancar_erro(self, conta_teste):
        conta_teste.depositar(50)
        with pytest.raises(SaldoInsuficienteError):
            conta_teste.sacar(100)
        assert conta_teste.saldo == 50

    def test_transferencia_com_sucesso(self, conta_teste, conta_destino):
        conta_teste.depositar(200)
        conta_teste.transferir(conta_destino, 50)

        assert conta_teste.saldo == 150
        assert conta_destino.saldo == 50
    
        assert "Transferência enviada" in conta_teste.historico[-1]["tipo"]
        assert "Transferência recebida" in conta_destino.historico[-1]["tipo"]

    def test_transferencia_sem_saldo_deve_falhar_atomicamente(self, conta_teste, conta_destino):
        conta_teste.depositar(10)
        
        with pytest.raises(SaldoInsuficienteError):
            conta_teste.transferir(conta_destino, 50)

        assert conta_teste.saldo == 10  # Saldo original mantido
        assert conta_destino.saldo == 0 # Destino não recebeu nada
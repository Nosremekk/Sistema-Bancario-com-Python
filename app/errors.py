class BankingError(Exception):
    pass

class SaldoInsuficienteError(BankingError):
    pass

class ValorInvalidoError(BankingError):
    pass
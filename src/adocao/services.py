class SistemaAdocao:
    """
    Gerente Geral (Facade). Coordena Repositórios, Estratégias e Domínio.
    
    Atributos:
        - repositorio: Instância de Repositorio.
        - calculadora: Instância de CalculadoraTaxas.
        - animais: Lista de objetos Animal.
        - adotantes: Lista de objetos Adotante.
        
    Métodos Principais:
        - cadastrar_animal(...)
        - cadastrar_adotante(...)
        - processar_reserva(adotante, animal)
        - efetivar_adocao(reserva)
        - gerar_relatorios()
    """
    pass
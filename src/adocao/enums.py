import enum

class StatusAnimal(enum.Enum):
    """Define os status possíveis de um animal no abrigo."""
    DISPONIVEL = "Disponível"
    RESERVADO = "Reservado"
    ADOTADO = "Adotado"
    DEVOLVIDO = "Devolvido"
    QUARENTENA = "Quarentena"
    INADOTAVEL = "Inadotável"

class PorteAnimal(enum.Enum):
    """Define os portes (tamanhos) de um animal."""
    P = "Pequeno"
    M = "Médio"
    G = "Grande"

class TipoMoradia(enum.Enum):
    """Define os tipos de moradia do adotante."""
    CASA = "Casa"
    APTO = "Apartamento"    
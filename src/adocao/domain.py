# --- 1. Entidades Principais (Domínio) ---

class Pessoa():
    """Classe base abstrata para representar uma pessoa no sistema."""
    pass

class Adotante(Pessoa):
    """
    Representa um adotante, com suas características e perfil
    para triagem.
    """
    pass

class Animal():
    """Classe base abstrata para todos os animais do abrigo."""
    pass

# --- 2. Entidades Animal Concretas ---

class Cachorro(Animal):
    """Representa um animal da espécie Cachorro."""
    pass

class Gato(Animal):
    """Representa um animal da espécie Gato."""
    pass

# --- 3. Entidades de Transação e Processo ---

class Reserva:
    """Modela a reserva de um animal por um adotante."""
    pass

class Adocao:
    """Registra a adoção formal de um animal."""
    pass

class FilaEspera:
    """Gerencia a fila de espera priorizada para um animal."""
    pass
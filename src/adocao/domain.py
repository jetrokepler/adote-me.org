from abc import ABC
from datetime import date, datetime
from typing import List, Dict, Any, Iterator
# Assumindo que o arquivo acima se chama enums.py
from .enums import StatusAnimal, PorteAnimal, TipoMoradia

# --- Mixins (Comportamentos Reutilizáveis) ---

class VacinavelMixin:
    """Adiciona capacidade de vacinação."""
    def __init__(self):
        # Inicializa o dicionário se a classe filha ainda não o fez
        if not hasattr(self, '_agenda_vacinas'):
            self._agenda_vacinas: Dict[str, date] = {}

    def vacinar(self, vacina: str):
        self._agenda_vacinas[vacina] = date.today()
        # Se for um Animal, registra no histórico
        if isinstance(self, Animal):
            self.adicionar_evento_historico(f"Vacinado com {vacina}")

class AdestravelMixin:
    """Adiciona capacidade de adestramento."""
    def __init__(self):
        self._nivel_adestramento: int = 0

    def treinar(self):
        self._nivel_adestramento += 1
        if isinstance(self, Animal):
            self.adicionar_evento_historico(f"Treinado. Nível atual: {self._nivel_adestramento}")

# --- Classes Base ---

class Pessoa(ABC):
    """Classe base abstrata para pessoas."""
    def __init__(self, nome: str, idade: int):
        self._nome = nome
        self._idade = idade

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def idade(self) -> int:
        return self._idade

class Adotante(Pessoa):
    """
    Representa o adotante com seus dados de moradia e perfil.
    """
    def __init__(self, nome: str, idade: int, moradia: TipoMoradia, 
                 area_util: float, experiencia_pets: bool, 
                 criancas_em_casa: bool, outros_animais: bool):
        super().__init__(nome, idade)
        self._moradia = moradia
        self._area_util = area_util
        self._experiencia_pets = experiencia_pets
        self._criancas_em_casa = criancas_em_casa
        self._outros_animais = outros_animais

    # Exemplo de verificação usando um objeto de configuração (dummy)
    def verificar_elegibilidade(self, politicas: Any) -> bool:
        """
        Verifica se o adotante atende às regras mínimas (ex: idade).
        """
        if self.idade < politicas.idade_minima_adotante:
            return False
        return True

    def __str__(self) -> str:
        return f"Adotante: {self.nome} ({self._moradia.value}, {self._area_util}m²)"

# --- Hierarquia de Animais ---

class Animal(ABC):
    """
    Classe base abstrata para Animais.
    Implementa ordenação, igualdade e iteração sobre histórico.
    """
    def __init__(self, id: int, nome: str, especie: str, raca: str, 
                 idade_meses: int, porte: PorteAnimal):
        self._id = id
        self._nome = nome
        self._especie = especie
        self._raca = raca
        self._idade_meses = idade_meses
        self._porte = porte
        
        # Atributos automáticos
        self._status = StatusAnimal.QUARENTENA
        self._data_entrada = date.today()
        self._historico_eventos: List[str] = []
        
        self.adicionar_evento_historico("Animal cadastrado no sistema.")

    # --- Encapsulamento (@property) ---
    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def status(self) -> StatusAnimal:
        return self._status

    @property
    def porte(self) -> PorteAnimal:
        return self._porte

    # --- Métodos de Negócio ---
    def adicionar_evento_historico(self, evento: str):
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        self._historico_eventos.append(f"[{timestamp}] {evento}")

    def validar_transicao_status(self, novo_status: StatusAnimal) -> bool:
        """Regra simples: não pode mudar para o status atual."""
        if self._status == novo_status:
            return False
        # Poderia ter regras complexas aqui (ex: INADOTAVEL não vira ADOTADO)
        return True

    def mudar_status(self, novo_status: StatusAnimal):
        if self.validar_transicao_status(novo_status):
            antigo = self._status
            self._status = novo_status
            self.adicionar_evento_historico(f"Status alterado: {antigo.name} -> {novo_status.name}")
        else:
            raise ValueError(f"Transição inválida para {novo_status.name}")

    # --- Métodos Especiais (Dunder Methods) ---
    
    def __str__(self) -> str:
        """Representação amigável (string)."""
        return f"[{self._id}] {self._nome} - {self._especie} ({self._status.value})"

    def __eq__(self, outro: object) -> bool:
        """Igualdade baseada no ID único."""
        if not isinstance(outro, Animal):
            return False
        return self._id == outro.id

    def __lt__(self, outro: 'Animal') -> bool:
        """
        Ordenação (Less Than) baseada na data de entrada.
        Útil para filas de prioridade ou ordenação de listas.
        """
        return self._data_entrada < outro._data_entrada

    def __iter__(self) -> Iterator[str]:
        """
        Permite iterar sobre o objeto Animal para ver seu histórico.
        Ex: for evento in animal: print(evento)
        """
        return iter(self._historico_eventos)

# --- Classes Concretas ---

class Cachorro(Animal, VacinavelMixin, AdestravelMixin):
    def __init__(self, id: int, nome: str, raca: str, idade_meses: int, 
                 porte: PorteAnimal, necessidade_passeio: int):
        # Inicializa Animal
        super().__init__(id, nome, "Cachorro", raca, idade_meses, porte)
        # Inicializa Mixins
        VacinavelMixin.__init__(self)
        AdestravelMixin.__init__(self)
        
        self._necessidade_passeio = necessidade_passeio # Nível 1 a 5, por exemplo

class Gato(Animal, VacinavelMixin):
    def __init__(self, id: int, nome: str, raca: str, idade_meses: int, 
                 porte: PorteAnimal, independencia: int):
        # Inicializa Animal
        super().__init__(id, nome, "Gato", raca, idade_meses, porte)
        # Inicializa Mixin (Gatos não são AdestravelMixin neste modelo)
        VacinavelMixin.__init__(self)
        
        self._independencia = independencia
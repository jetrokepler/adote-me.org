from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .enums import StatusAnimal, PorteAnimal, TipoMoradia

# --- CLASSES PESSOA ---

class Pessoa(ABC):
    def __init__(self, nome: str, contato: str):
        self._nome = nome
        self._contato = contato

    @property
    def nome(self) -> str: return self._nome
    
    @property
    def contato(self) -> str: return self._contato

class Adotante(Pessoa):
    def __init__(self, nome: str, contato: str, moradia: TipoMoradia, tem_criancas: bool):
        super().__init__(nome, contato)
        self._moradia = moradia
        self._tem_criancas = tem_criancas

    @property
    def moradia(self) -> TipoMoradia: return self._moradia

    # --- NOVO: Métodos para JSON ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome": self._nome,
            "contato": self._contato,
            "moradia": self._moradia.value,
            "tem_criancas": self._tem_criancas
        }

    @classmethod
    def from_dict(cls, dados: Dict[str, Any]):
        return cls(
            nome=dados["nome"],
            contato=dados["contato"],
            moradia=TipoMoradia(dados["moradia"]),
            tem_criancas=dados["tem_criancas"]
        )

    def __str__(self):
        criancas = "Com crianças" if self._tem_criancas else "Sem crianças"
        return f"[Adotante] {self.nome} ({self._moradia.value}) - {criancas}"

# --- CLASSES ANIMAL ---

class Animal(ABC):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal):
        self._nome = nome
        self._raca = raca
        self._status = status
        self._porte = porte

    @property
    def nome(self) -> str: return self._nome
    @property
    def status(self) -> StatusAnimal: return self._status
    @property
    def porte(self) -> PorteAnimal: return self._porte

    def mudar_status(self, novo_status: StatusAnimal):
        self._status = novo_status

    # --- NOVO: Contrato para JSON ---
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass
    
    @staticmethod
    def from_dict(dados: Dict[str, Any]):
        tipo = dados.get("tipo_classe")
        if tipo == "Cachorro":
            return Cachorro.from_dict_concreto(dados)
        elif tipo == "Gato":
            return Gato.from_dict_concreto(dados)
        return None

class Cachorro(Animal):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, precisa_passeio: bool):
        super().__init__(nome, raca, status, porte)
        self._precisa_passeio = precisa_passeio

    # --- NOVO: Métodos para JSON ---
    def to_dict(self):
        return {
            "tipo_classe": "Cachorro",
            "nome": self._nome,
            "raca": self._raca,
            "status": self._status.value,
            "porte": self._porte.value,
            "precisa_passeio": self._precisa_passeio
        }

    @classmethod
    def from_dict_concreto(cls, dados):
        return cls(
            nome=dados["nome"],
            raca=dados["raca"],
            status=StatusAnimal(dados["status"]),
            porte=PorteAnimal(dados["porte"]),
            precisa_passeio=dados["precisa_passeio"]
        )

    def __str__(self):
        passeio = "Precisa passeio" if self._precisa_passeio else "Caseiro"
        return f"🐶 {self.nome} ({self._raca}) - {self._status.value} - {passeio}"

class Gato(Animal):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, independencia: int):
        super().__init__(nome, raca, status, porte)
        self._independencia = independencia

    # --- NOVO: Métodos para JSON ---
    def to_dict(self):
        return {
            "tipo_classe": "Gato",
            "nome": self._nome,
            "raca": self._raca,
            "status": self._status.value,
            "porte": self._porte.value,
            "independencia": self._independencia
        }

    @classmethod
    def from_dict_concreto(cls, dados):
        return cls(
            nome=dados["nome"],
            raca=dados["raca"],
            status=StatusAnimal(dados["status"]),
            porte=PorteAnimal(dados["porte"]),
            independencia=dados["independencia"]
        )

    def __str__(self):
        return f"🐱 {self.nome} ({self._raca}) - {self._status.value} - Nível Indep.: {self._independencia}"
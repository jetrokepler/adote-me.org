from abc import ABC
from typing import List, Optional
from .enums import StatusAnimal, PorteAnimal, TipoMoradia

# --- CLASSES PESSOA ---

class Pessoa(ABC):
    def __init__(self, nome: str, contato: str):
        self._nome = nome
        self._contato = contato

    @property
    def nome(self) -> str:
        return self._nome
    
    @property
    def contato(self) -> str:
        return self._contato

class Adotante(Pessoa):
    def __init__(self, nome: str, contato: str, moradia: TipoMoradia, tem_criancas: bool):
        super().__init__(nome, contato)
        self._moradia = moradia
        self._tem_criancas = tem_criancas

    @property
    def moradia(self) -> TipoMoradia:
        return self._moradia

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
    def nome(self) -> str: 
        return self._nome

    @property
    def status(self) -> StatusAnimal: 
        return self._status

    @property
    def porte(self) -> PorteAnimal:
        return self._porte

    def mudar_status(self, novo_status: StatusAnimal):
        # Aqui você pode adicionar validações futuras (ex: INADOTAVEL não vira DISPONIVEL)
        self._status = novo_status

class Cachorro(Animal):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, precisa_passeio: bool):
        super().__init__(nome, raca, status, porte)
        self._precisa_passeio = precisa_passeio

    def __str__(self):
        passeio = "Precisa passeio" if self._precisa_passeio else "Caseiro"
        return f"🐶 {self.nome} ({self._raca}) - {self._status.value} - {passeio}"

class Gato(Animal):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, independencia: int):
        super().__init__(nome, raca, status, porte)
        self._independencia = independencia # Nível 0 a 5

    def __str__(self):
        return f"🐱 {self.nome} ({self._raca}) - {self._status.value} - Nível Indep.: {self._independencia}"
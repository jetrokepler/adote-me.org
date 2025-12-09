from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import date, datetime
from .enums import StatusAnimal, PorteAnimal, TipoMoradia

class VacinavelMixin:
    def __init__(self):
        self.agenda_vacinas: Dict[str, str] = {}

    def vacinar(self, nome_vacina: str):
        self.agenda_vacinas[nome_vacina] = date.today().isoformat()
        if isinstance(self, Animal):
            self.adicionar_evento(f"Vacinado contra {nome_vacina}")

class AdestravelMixin:
    def __init__(self):
        self.nivel_adestramento: int = 0

    def treinar(self):
        self.nivel_adestramento += 1
        if isinstance(self, Animal):
            self.adicionar_evento(f"Treinado. Nível atual: {self.nivel_adestramento}")


class Pessoa(ABC):
    def __init__(self, nome: str, contato: str):
        self._nome = nome
        self._contato = contato

    @property
    def nome(self): return self._nome
    @property
    def contato(self): return self._contato

class Adotante(Pessoa):
    def __init__(self, nome: str, contato: str, idade: int, moradia: TipoMoradia, area_util: float, tem_criancas: bool):
        super().__init__(nome, contato)
        self._idade = idade
        self._moradia = moradia
        self._area_util = area_util
        self._tem_criancas = tem_criancas

    @property
    def idade(self): return self._idade
    @property
    def moradia(self): return self._moradia
    @property
    def area_util(self): return self._area_util
    @property
    def tem_criancas(self): return self._tem_criancas

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nome": self._nome,
            "contato": self._contato,
            "idade": self._idade,
            "moradia": self._moradia.value,
            "area_util": self._area_util,
            "tem_criancas": self._tem_criancas
        }

    @classmethod
    def from_dict(cls, dados: Dict[str, Any]):
        return cls(
            nome=dados["nome"],
            contato=dados["contato"],
            idade=dados.get("idade", 18),
            moradia=TipoMoradia(dados["moradia"]),
            area_util=dados.get("area_util", 0.0),
            tem_criancas=dados.get("tem_criancas", False)
        )

    def __str__(self):
        return f"[Adotante] {self.nome}, {self._idade} anos ({self._moradia.value}, {self._area_util}m²)"


class Animal(ABC):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, temperamento: List[str]):
        self._nome = nome
        self._raca = raca
        self._status = status
        self._porte = porte
        self._temperamento = temperamento
        self.historico_eventos: List[str] = []
        self.adicionar_evento("Animal cadastrado no sistema.")

    @property
    def nome(self): return self._nome
    @property
    def status(self): return self._status
    @property
    def porte(self): return self._porte
    @property
    def temperamento(self): return self._temperamento

    def adicionar_evento(self, descricao: str):
        """Registra um evento com data e hora."""
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.historico_eventos.append(f"[{data_hora}] {descricao}")

    def pode_mudar_para(self, novo_status: StatusAnimal) -> bool:
        atual = self._status
        if atual == novo_status: return True
        if atual == StatusAnimal.DISPONIVEL:
            return novo_status in [StatusAnimal.RESERVADO, StatusAnimal.ADOTADO, StatusAnimal.INADOTAVEL]
        if atual == StatusAnimal.RESERVADO:
            return novo_status in [StatusAnimal.ADOTADO, StatusAnimal.DISPONIVEL]
        if atual == StatusAnimal.ADOTADO:
            return novo_status == StatusAnimal.DEVOLVIDO
        if atual == StatusAnimal.DEVOLVIDO:
             return novo_status in [StatusAnimal.QUARENTENA, StatusAnimal.DISPONIVEL, StatusAnimal.INADOTAVEL]
        if atual == StatusAnimal.QUARENTENA:
            return novo_status in [StatusAnimal.DISPONIVEL, StatusAnimal.INADOTAVEL]
        return False

    def mudar_status(self, novo_status: StatusAnimal):
        if not self.pode_mudar_para(novo_status):
            raise ValueError(f"Transição inválida: {self._status.value} -> {novo_status.value}")
        
        # ADICIONADO: Registro no histórico
        self.adicionar_evento(f"Status alterado: {self._status.value} -> {novo_status.value}")
        self._status = novo_status

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]: pass
    
    @staticmethod
    def from_dict(dados: Dict[str, Any]):
        tipo = dados.get("tipo_classe")
        if tipo == "Cachorro": return Cachorro.from_dict_concreto(dados)
        elif tipo == "Gato": return Gato.from_dict_concreto(dados)
        return None

class Cachorro(Animal, VacinavelMixin, AdestravelMixin):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, temperamento: List[str], precisa_passeio: bool):
        super().__init__(nome, raca, status, porte, temperamento)
        VacinavelMixin.__init__(self)
        AdestravelMixin.__init__(self)
        self._precisa_passeio = precisa_passeio

    def to_dict(self):
        return {
            "tipo_classe": "Cachorro",
            "nome": self._nome,
            "raca": self._raca,
            "status": self._status.value,
            "porte": self._porte.value,
            "temperamento": self._temperamento,
            "precisa_passeio": self._precisa_passeio,
            # Novos campos de persistência dos Mixins/Histórico
            "historico": self.historico_eventos,
            "vacinas": self.agenda_vacinas,
            "nivel_adestramento": self.nivel_adestramento
        }

    @classmethod
    def from_dict_concreto(cls, dados):
        obj = cls(
            nome=dados["nome"],
            raca=dados["raca"],
            status=StatusAnimal(dados["status"]),
            porte=PorteAnimal(dados["porte"]),
            temperamento=dados.get("temperamento", []),
            precisa_passeio=dados["precisa_passeio"]
        )
        obj.historico_eventos = dados.get("historico", [])
        obj.agenda_vacinas = dados.get("vacinas", {})
        obj.nivel_adestramento = dados.get("nivel_adestramento", 0)
        return obj
    
    def __str__(self):
        return f"🐶 {self.nome} ({self._status.value}) - {self._porte.value}"

class Gato(Animal, VacinavelMixin):
    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, temperamento: List[str], independencia: int):
        super().__init__(nome, raca, status, porte, temperamento)
        VacinavelMixin.__init__(self)
        self._independencia = independencia

    def to_dict(self):
        return {
            "tipo_classe": "Gato",
            "nome": self._nome,
            "raca": self._raca,
            "status": self._status.value,
            "porte": self._porte.value,
            "temperamento": self._temperamento,
            "independencia": self._independencia,
            # Novos campos
            "historico": self.historico_eventos,
            "vacinas": self.agenda_vacinas
        }

    @classmethod
    def from_dict_concreto(cls, dados):
        obj = cls(
            nome=dados["nome"],
            raca=dados["raca"],
            status=StatusAnimal(dados["status"]),
            porte=PorteAnimal(dados["porte"]),
            temperamento=dados.get("temperamento", []),
            independencia=dados["independencia"]
        )
        obj.historico_eventos = dados.get("historico", [])
        obj.agenda_vacinas = dados.get("vacinas", {})
        return obj
        
    def __str__(self):
        return f"🐱 {self.nome} ({self._status.value}) - {self._porte.value}"
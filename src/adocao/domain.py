from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from .enums import StatusAnimal, PorteAnimal, TipoMoradia
from .exceptions import TransicaoStatusError

class VacinavelMixin:
    """Mixin que adiciona funcionalidades de vacinação a uma classe.

    Attributes:
        agenda_vacinas (Dict[str, str]): Registro de vacinas aplicadas (Nome -> Data).
    """

    def __init__(self) -> None:
        """Inicializa o mixin de vacinação."""
        self.agenda_vacinas: Dict[str, str] = {} 

    def vacinar(self, nome_vacina: str) -> None:
        """Registra a aplicação de uma vacina e adiciona evento ao histórico se for Animal.

        Args:
            nome_vacina (str): O nome da vacina aplicada.
        """
        self.agenda_vacinas[nome_vacina] = datetime.now().strftime("%Y-%m-%d")
        if isinstance(self, Animal): 
            self.adicionar_evento(f"Vacinado contra {nome_vacina}")

class AdestravelMixin:
    """Mixin que adiciona funcionalidades de adestramento a uma classe.

    Attributes:
        nivel_adestramento (int): Nível atual de adestramento (0 = sem treino).
    """

    def __init__(self) -> None:
        """Inicializa o mixin de adestramento."""
        self.nivel_adestramento: int = 0

    def treinar(self) -> None:
        """Incrementa o nível de adestramento e registra evento se for Animal."""
        self.nivel_adestramento += 1
        if isinstance(self, Animal): 
            self.adicionar_evento(f"Treinado. Nível atual: {self.nivel_adestramento}")

class Pessoa(ABC):
    """Classe abstrata base para representar uma pessoa no sistema.

    Attributes:
        _nome (str): Nome completo da pessoa.
        _contato (str): Informação de contato (e-mail ou telefone).
    """

    def __init__(self, nome: str, contato: str) -> None:
        """Inicializa uma nova Pessoa.

        Args:
            nome (str): Nome da pessoa.
            contato (str): Contato da pessoa.
        """
        self._nome = nome
        self._contato = contato

    @property
    def nome(self) -> str:
        """str: Retorna o nome da pessoa."""
        return self._nome

    @property
    def contato(self) -> str:
        """str: Retorna o contato da pessoa."""
        return self._contato

class Adotante(Pessoa):
    """Representa um potencial adotante no sistema.

    Attributes:
        _idade (int): Idade do adotante.
        _moradia (TipoMoradia): Tipo de moradia (Casa, Apartamento, etc.).
        _area_util (float): Área útil da moradia em m².
        _tem_criancas (bool): Indica se há crianças na residência.
    """

    def __init__(self, nome: str, contato: str, idade: int, moradia: TipoMoradia, area_util: float, tem_criancas: bool) -> None:
        """Inicializa um novo Adotante.

        Args:
            nome (str): Nome do adotante.
            contato (str): Contato do adotante.
            idade (int): Idade do adotante.
            moradia (TipoMoradia): Tipo de residência.
            area_util (float): Área disponível.
            tem_criancas (bool): Se possui crianças.
        """
        super().__init__(nome, contato)
        self._idade = idade
        self._moradia = moradia
        self._area_util = area_util
        self._tem_criancas = tem_criancas

    @property
    def idade(self) -> int:
        """int: Retorna a idade do adotante."""
        return self._idade

    @property
    def moradia(self) -> TipoMoradia:
        """TipoMoradia: Retorna o tipo de moradia."""
        return self._moradia

    @property
    def area_util(self) -> float:
        """float: Retorna a área útil da moradia."""
        return self._area_util

    @property
    def tem_criancas(self) -> bool:
        """bool: Retorna True se tiver crianças, False caso contrário."""
        return self._tem_criancas

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o adotante para um dicionário.

        Returns:
            Dict[str, Any]: Dados do adotante.
        """
        return {
            "nome": self._nome,
            "contato": self._contato,
            "idade": self._idade,
            "moradia": self._moradia.value,
            "area_util": self._area_util,
            "tem_criancas": self._tem_criancas
        }

    @classmethod
    def from_dict(cls, dados: Dict[str, Any]) -> 'Adotante':
        """Cria uma instância de Adotante a partir de um dicionário.

        Args:
            dados (Dict[str, Any]): Dicionário com os dados.

        Returns:
            Adotante: Instância criada.
        """
        return cls(
            nome=dados["nome"],
            contato=dados["contato"],
            idade=dados.get("idade", 18),
            moradia=TipoMoradia(dados["moradia"]),
            area_util=dados.get("area_util", 0.0),
            tem_criancas=dados.get("tem_criancas", False)
        )

    def __str__(self) -> str:
        """Retorna representação textual do Adotante."""
        return f"[Adotante] {self.nome}, {self._idade} anos ({self._moradia.value}, {self._area_util}m²)"

class FilaEspera:
    """Gerencia a fila de interessados em um animal específico.

    Attributes:
        interessados (List[Dict[str, Any]]): Lista de dicionários contendo adotante, score e data.
    """

    def __init__(self) -> None:
        """Inicializa a fila de espera vazia."""
        self.interessados: List[Dict[str, Any]] = []

    def adicionar(self, adotante: Adotante, score: int) -> None:
        """Adiciona um adotante à fila, ordenando por score (decrescente) e data (crescente).

        Args:
            adotante (Adotante): O interessado.
            score (int): Pontuação de compatibilidade.
        """
        for item in self.interessados:
            if item['adotante'].nome == adotante.nome: 
                return 
        
        novo_item = {
            'adotante': adotante,
            'score': score,
            'data_entrada': datetime.now().isoformat()
        }
        self.interessados.append(novo_item)
        
        self.interessados.sort(key=lambda x: (-x['score'], x['data_entrada']))

    def proximo(self) -> Optional[Adotante]:
        """Retorna e remove o próximo adotante da fila (maior prioridade).

        Returns:
            Optional[Adotante]: O próximo da fila ou None se estiver vazia.
        """
        if self.interessados:
            return self.interessados.pop(0)['adotante']
        return None

    def __len__(self) -> int: 
        """Retorna o tamanho da fila."""
        return len(self.interessados)

    def to_list_dict(self) -> List[Dict[str, Any]]:
        """Serializa a fila para lista de dicionários.

        Returns:
            List[Dict[str, Any]]: Lista serializada.
        """
        lista_salva = []
        for item in self.interessados:
            lista_salva.append({
                'adotante': item['adotante'].to_dict(),
                'score': item['score'],
                'data_entrada': item['data_entrada']
            })
        return lista_salva

class Animal(ABC):
    """Classe abstrata base para animais no sistema.

    Attributes:
        _nome (str): Nome do animal.
        _raca (str): Raça do animal.
        _status (StatusAnimal): Status atual (Disponível, Adotado, etc.).
        _porte (PorteAnimal): Porte do animal.
        _temperamento (List[str]): Lista de traços de temperamento.
        historico_eventos (List[str]): Log de eventos do animal.
        data_reserva (Optional[str]): Data da reserva, se houver.
        nome_reservante (Optional[str]): Nome de quem reservou, se houver.
        fila_espera (FilaEspera): Fila de interessados no animal.
    """

    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, temperamento: List[str]) -> None:
        """Inicializa um Animal.

        Args:
            nome (str): Nome.
            raca (str): Raça.
            status (StatusAnimal): Status inicial.
            porte (PorteAnimal): Porte.
            temperamento (List[str]): Temperamentos.
        """
        self._nome = nome
        self._raca = raca
        self._status = status
        self._porte = porte
        self._temperamento = temperamento
        
        self.historico_eventos: List[str] = []
        self.data_reserva: Optional[str] = None
        self.nome_reservante: Optional[str] = None
        self.fila_espera = FilaEspera()
        
        if len(self.historico_eventos) == 0:
            self.adicionar_evento("Cadastrado no sistema.")

    @property
    def nome(self) -> str:
        """str: Retorna o nome do animal."""
        return self._nome

    @property
    def status(self) -> StatusAnimal:
        """StatusAnimal: Retorna o status atual."""
        return self._status

    @property
    def porte(self) -> PorteAnimal:
        """PorteAnimal: Retorna o porte."""
        return self._porte

    @property
    def temperamento(self) -> List[str]:
        """List[str]: Retorna a lista de temperamentos."""
        return self._temperamento

    def adicionar_evento(self, descricao: str) -> None:
        """Registra um evento no histórico do animal.

        Args:
            descricao (str): Descrição do evento.
        """
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.historico_eventos.append(f"[{data_hora}] {descricao}")

    def pode_mudar_para(self, novo_status: StatusAnimal) -> bool:
        """Verifica se a transição de status é permitida pelas regras de negócio.

        Args:
            novo_status (StatusAnimal): O status destino.

        Returns:
            bool: True se a transição for válida, False caso contrário.
        """
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

    def mudar_status(self, novo_status: StatusAnimal) -> None:
        """Altera o status do animal se a transição for válida.

        Args:
            novo_status (StatusAnimal): O novo status.

        Raises:
            TransicaoStatusError: Se a transição não for permitida.
        """
        if not self.pode_mudar_para(novo_status):
            raise TransicaoStatusError(f"Transição inválida: {self._status.value} -> {novo_status.value}")
        
        if self._status == StatusAnimal.RESERVADO and novo_status != StatusAnimal.RESERVADO:
            self.data_reserva = None
            self.nome_reservante = None

        self.adicionar_evento(f"Status alterado: {self._status.value} -> {novo_status.value}")
        self._status = novo_status

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializa o animal para dicionário (abstrato)."""
        pass
    
    @staticmethod
    def from_dict(dados: Dict[str, Any]) -> Optional['Animal']:
        """Factory method para criar Cachorro ou Gato baseado nos dados.

        Args:
            dados (Dict[str, Any]): Dicionário com os dados.

        Returns:
            Optional[Animal]: Instância de Cachorro ou Gato, ou None se tipo inválido.
        """
        tipo = dados.get("tipo_classe")
        if tipo == "Cachorro": return Cachorro.from_dict_concreto(dados)
        elif tipo == "Gato": return Gato.from_dict_concreto(dados)
        return None

class Cachorro(Animal, VacinavelMixin, AdestravelMixin):
    """Representa um cachorro no sistema.

    Attributes:
        _precisa_passeio (bool): Indica se o cachorro precisa de passeios frequentes.
    """

    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, temperamento: List[str], precisa_passeio: bool) -> None:
        """Inicializa um Cachorro.

        Args:
            nome (str): Nome.
            raca (str): Raça.
            status (StatusAnimal): Status.
            porte (PorteAnimal): Porte.
            temperamento (List[str]): Temperamentos.
            precisa_passeio (bool): Necessidade de passeio.
        """
        super().__init__(nome, raca, status, porte, temperamento)
        VacinavelMixin.__init__(self)
        AdestravelMixin.__init__(self)
        self._precisa_passeio = precisa_passeio

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o cachorro para dicionário.

        Returns:
            Dict[str, Any]: Dados do cachorro.
        """
        return {
            "tipo_classe": "Cachorro",
            "nome": self._nome,
            "raca": self._raca,
            "status": self._status.value,
            "porte": self._porte.value,
            "temperamento": self._temperamento,
            "precisa_passeio": self._precisa_passeio,
            "historico": self.historico_eventos,
            "vacinas": self.agenda_vacinas,
            "nivel_adestramento": self.nivel_adestramento,
            "data_reserva": self.data_reserva,
            "nome_reservante": self.nome_reservante, 
            "fila_espera": self.fila_espera.to_list_dict()
        }

    @classmethod
    def from_dict_concreto(cls, dados: Dict[str, Any]) -> 'Cachorro':
        """Cria um Cachorro a partir de um dicionário.

        Args:
            dados (Dict[str, Any]): Dados do cachorro.

        Returns:
            Cachorro: Instância criada.
        """
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
        obj.data_reserva = dados.get("data_reserva")
        obj.nome_reservante = dados.get("nome_reservante")
        
        lista_fila = dados.get("fila_espera", [])
        for item in lista_fila:
            adotante = Adotante.from_dict(item['adotante'])
            obj.fila_espera.interessados.append({
                'adotante': adotante, 
                'score': item['score'], 
                'data_entrada': item['data_entrada']
            })
        return obj
    
    def __str__(self) -> str:
        """Retorna representação textual do Cachorro."""
        return f"🐶 {self.nome} ({self._status.value}) - {self._porte.value}"

class Gato(Animal, VacinavelMixin):
    """Representa um gato no sistema.

    Attributes:
        _independencia (int): Nível de independência do gato (0 a 5).
    """

    def __init__(self, nome: str, raca: str, status: StatusAnimal, porte: PorteAnimal, temperamento: List[str], independencia: int) -> None:
        """Inicializa um Gato.

        Args:
            nome (str): Nome.
            raca (str): Raça.
            status (StatusAnimal): Status.
            porte (PorteAnimal): Porte.
            temperamento (List[str]): Temperamentos.
            independencia (int): Grau de independência.
        """
        super().__init__(nome, raca, status, porte, temperamento)
        VacinavelMixin.__init__(self)
        self._independencia = independencia

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o gato para dicionário.

        Returns:
            Dict[str, Any]: Dados do gato.
        """
        return {
            "tipo_classe": "Gato",
            "nome": self._nome,
            "raca": self._raca,
            "status": self._status.value,
            "porte": self._porte.value,
            "temperamento": self._temperamento,
            "independencia": self._independencia,
            "historico": self.historico_eventos,
            "vacinas": self.agenda_vacinas,
            "data_reserva": self.data_reserva,
            "nome_reservante": self.nome_reservante,
            "fila_espera": self.fila_espera.to_list_dict()
        }

    @classmethod
    def from_dict_concreto(cls, dados: Dict[str, Any]) -> 'Gato':
        """Cria um Gato a partir de um dicionário.

        Args:
            dados (Dict[str, Any]): Dados do gato.

        Returns:
            Gato: Instância criada.
        """
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
        obj.data_reserva = dados.get("data_reserva")
        obj.nome_reservante = dados.get("nome_reservante")
        
        lista_fila = dados.get("fila_espera", [])
        for item in lista_fila:
            adotante = Adotante.from_dict(item['adotante'])
            obj.fila_espera.interessados.append({
                'adotante': adotante, 
                'score': item['score'], 
                'data_entrada': item['data_entrada']
            })
        return obj
        
    def __str__(self) -> str:
        """Retorna representação textual do Gato."""
        return f"🐱 {self.nome} ({self._status.value}) - {self._porte.value}"
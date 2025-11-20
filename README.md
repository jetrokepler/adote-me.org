# 🐾 adote-me.org

Este é um sistema de linha de comando (CLI) para gerenciar o fluxo completo de um abrigo de animais. Ele controla desde o cadastro de animais e a triagem de adotantes até o processo de reserva, adoção e devolução.

# ⛳ Objetivo

O objetivo principal é aplicar conceitos de Programação Orientada a Objetos (POO) para construir um sistema robusto e flexível. O projeto foca em modelar entidades do mundo real, gerenciar seus estados e implementar regras de negócio complexas de forma organizada e testável.

## Estrutura de arquivos

```
📁 projeto_adocao/
├── 📄 .gitignore
├── 📄 README.md
├── 📄 requirements.txt
│
├── 📁 src/
│   └── 📁 adocao/
│       ├── 📄 __init__.py
│       ├── 📄 enums.py         
│       ├── 📄 domain.py        
│       ├── 📄 strategies.py    
│       ├── 📄 repositories.py  
│       ├── 📄 services.py      
│       └── 📄 main.py          
│
└── 📁 tests/
    ├── 📄 __init__.py
    ├── 📄 test_domain.py     
    ├── 📄 test_services.py   
    └── 📄 test_strategies.py 
```

# 🏛️ Arquitetura

```mermaid
classDiagram
    direction LR

    %% --- 1. Enumerações e Tipos ---
    class StatusAnimal {
        <<enumeration>>
        DISPONIVEL
        RESERVADO
        ADOTADO
        DEVOLVIDO
        QUARENTENA
        INADOTAVEL
    }
    class PorteAnimal {
        <<enumeration>>
        P
        M
        G
    }
    class TipoMoradia {
        <<enumeration>>
        CASA
        APTO
    }

    %% --- 2. Entidades Principais ---
    class Pessoa {
        <<abstract>>
        -nome: str
        -idade: int
    }
    class Adotante {
        -moradia: TipoMoradia
        -area_util: float
        -experiencia_pets: bool
        -criancas_em_casa: bool
        -outros_animais: bool
        +verificar_elegibilidade(politicas) bool
    }
    Pessoa <|-- Adotante
    Adotante --> TipoMoradia

    class Animal {
        <<abstract>>
        -id: int
        -nome: str
        -especie: str
        -raca: str
        -idade_meses: int
        -porte: PorteAnimal
        -status: StatusAnimal
        -historico_eventos: list
        -data_entrada: date
        +mudar_status(novo_status)
        +validar_transicao_status(novo_status) bool
        +__str__() str
        +__lt__(outro) bool
        +__iter__() Iterator
    }
    Animal --> PorteAnimal
    Animal --> StatusAnimal

    class VacinavelMixin {
        <<mixin>>
        -agenda_vacinas: dict
        +vacinar(vacina)
    }
    class AdestravelMixin {
        <<mixin>>
        -nivel_adestramento: int
        +treinar()
    }

    class Cachorro {
        -necessidade_passeio: int
    }
    class Gato {
        -independencia: int
    }
    Animal <|-- Cachorro
    Animal <|-- Gato
    VacinavelMixin <|.. Cachorro
    AdestravelMixin <|.. Cachorro
    VacinavelMixin <|.. Gato

    %% --- 3. Entidades de Transação ---
    class Reserva {
        -data_reserva: datetime
        -data_expiracao: datetime
        +esta_expirada() bool
    }
    class Adocao {
        -data_adocao: datetime
        -taxa_calculada: float
        -contrato: str
    }
    class Devolucao {
        -data_devolucao: datetime
        -motivo: str
    }
    class FilaEspera {
        -fila: PriorityQueue
        +adicionar(adotante, pontuacao)
        +proximo() Adotante
        +__len__() int
    }

    %% --- 4. Padrões de Projeto ---
    
    %% Strategy (Taxa)
    class BaseFeeStrategy {
        <<interface>>
        +calcular_taxa(animal) float
    }
    class SeniorFee { +calcular_taxa(animal) float }
    class PuppyFee { +calcular_taxa(animal) float }
    class SpecialCareFee { +calcular_taxa(animal) float }
    class DefaultFee { +calcular_taxa(animal) float }
    BaseFeeStrategy <|.. SeniorFee
    BaseFeeStrategy <|.. PuppyFee
    BaseFeeStrategy <|.. SpecialCareFee
    BaseFeeStrategy <|.. DefaultFee

    %% Repository (Interfaces)
    class AnimalRepository {
        <<interface>>
        +get(id)
        +add(animal)
        +list()
    }
    class AdotanteRepository {
        <<interface>>
        +get(id)
        +add(adotante)
        +list()
    }
    class AdocaoRepository {
        <<interface>>
        +get(id)
        +add(adocao)
        +list()
    }
    
    %% Repository (Implementações)
    class JsonAnimalRepository { +JsonAnimalRepository(path) }
    class SqliteAnimalRepository { +SqliteAnimalRepository(conn) }
    class JsonAdotanteRepository { +JsonAdotanteRepository(path) }
    class SqliteAdotanteRepository { +SqliteAdotanteRepository(conn) }
    
    AnimalRepository <|.. JsonAnimalRepository
    AnimalRepository <|.. SqliteAnimalRepository
    AdotanteRepository <|.. JsonAdotanteRepository
    AdotanteRepository <|.. SqliteAdotanteRepository
    %% ... (O mesmo para AdocaoRepository)


    %% --- 5. Serviços e Configuração ---
    class Configuracoes {
        +idade_minima_adotante: int
        +duracao_reserva_horas: int
        +pesos_compatibilidade: dict
        +carregar_settings(arquivo)
    }
    class TriagemService {
        +calcular_compatibilidade(adotante, animal, config) int
        +validar_politicas(adotante, animal, config) bool
    }
    class SistemaAdocao {
        -repo_animais: AnimalRepository
        -repo_adotantes: AdotanteRepository
        -config: Configuracoes
        +cadastrar_animal()
        +cadastrar_adotante()
        +reservar_animal(adotante_id, animal_id)
        +efetivar_adocao(reserva_id, estrategia_taxa)
        +registrar_devolucao()
        +processar_expiracoes_reserva()
        +gerar_relatorio_top5_compatibilidade()
    }
    
    %% --- 6. Exceções ---
    class Exception { <<external>> }
    class ReservaInvalidaError {}
    class TransicaoDeEstadoInvalidaError {}
    class PoliticaNaoAtendidaError {}
    class RepositorioError {}
    Exception <|-- ReservaInvalidaError
    Exception <|-- TransicaoDeEstadoInvalidaError
    Exception <|-- PoliticaNaoAtendidaError
    Exception <|-- RepositorioError


    %% --- 7. Relacionamentos Principais ---
    SistemaAdocao --> "1" Configuracoes
    SistemaAdocao --> "1" AnimalRepository
    SistemaAdocao --> "1" AdotanteRepository
    SistemaAdocao --> "1" AdocaoRepository
    SistemaAdocao --> "1" TriagemService
    SistemaAdocao ..> BaseFeeStrategy : usa

    TriagemService --> Configuracoes

    Reserva o-- "1" Adotante
    Reserva o-- "1" Animal
    
    Adocao o-- "1" Adotante
    Adocao o-- "1" Animal
    
    Devolucao o-- "1" Adocao
    
    FilaEspera o-- "1" Animal
    FilaEspera ..> Adotante : "mantém na fila"
<div align="center">

# 🐾 adote-me.org

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python\&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-tests-green?logo=pytest)
![POO](https://img.shields.io/badge/Paradigma-POO-purple)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![License](https://img.shields.io/badge/License-MIT-brightgreen)
![Contributions](https://img.shields.io/badge/Contribui%C3%A7%C3%B5es-Bem--vindas-orange)

Este é um sistema de linha de comando (CLI) para gerenciar o fluxo completo de um abrigo de animais. Ele controla desde o cadastro de animais e a triagem de adotantes até o processo de reserva, adoção e devolução.

# ⛳ Objetivo

O objetivo principal é aplicar conceitos de Programação Orientada a Objetos (POO) para construir um sistema robusto e flexível. O projeto foca em modelar entidades do mundo real, gerenciar seus estados e implementar regras de negócio complexas de forma organizada e testável.

</div>

## Estrutura de arquivos

```
📁 ADOTE-ME.ORG/
│ 
├── 📄 .gitignore
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 pytest.ini
├── 📄 seed.py
├── 📄 settings.json
├── 📄 adocao.db
├── 📄 adotantes.json
├── 📄 animais.json
│
├── 📁 dados/
│    └── 📄 historico_eventos.log
│
├── 📁 relatorios/
│    └── 📄 relatorio_2025-12-15_01-58-12.txt
|
├── 📁 src/
│    └── 📁 adocao/
│         ├── 📄 __init__.py
│         ├── 📄 enums.py
│         ├── 📄 domain.py
│         ├── 📄 strategies.py
│         ├── 📄 repositories.py
│         ├── 📄 services.py
│         ├── 📄 exceptions.py
│         └── 📄 main.py
│
├── 📁 tests/
     ├── 📄 __init__.py
     ├── 📄 test_domain.py
     ├── 📄 test_fila_priorizada.py
     ├── 📄 test_observer.py
     ├── 📄 test_services.py
     └── 📄 test_strategies.py
```



# 🎡 Funcionamento

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/jetrokepler/adote-me.org.git
cd seu-projeto
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 🌳 Semeando o db

```bash
python seed.py
```


### 🧪 Executando os Testes

Todos os testes são feitos com **Pytest**:

```bash
pytest
```

Com relatório mais detalhado:

```bash
pytest -v
```

### 🧪 Modo on

Esse é o comando que incializa o progama.

```bash
python src.adocao.main
```


# 🏛️ Arquitetura


```mermaid
classDiagram
    %% --- ENUMS ---
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

    %% --- MIXINS ---
    class VacinavelMixin {
        +agenda_vacinas: Dict
        +__init__()
        +vacinar(nome_vacina)
    }

    class AdestravelMixin {
        +nivel_adestramento: int
        +__init__()
        +treinar()
    }

    %% --- DOMÍNIO: PESSOAS ---
    class Pessoa {
        <<abstract>>
        -_nome: str
        -_contato: str
        +__init__(nome, contato)
        +nome() str
        +contato() str
    }

    class Adotante {
        -_idade: int
        -_moradia: TipoMoradia
        -_area_util: float
        -_tem_criancas: bool
        +__init__(nome, contato, idade, moradia, area, kids)
        +idade() int
        +moradia() TipoMoradia
        +area_util() float
        +tem_criancas() bool
        +to_dict() Dict
        +from_dict(dados) Adotante$
        +__str__() str
    }

    Pessoa <|-- Adotante

    %% --- DOMÍNIO: ANIMAIS ---
    class FilaEspera {
        +interessados: List
        +__init__()
        +adicionar(adotante, score)
        +proximo() Adotante
        +__len__() int
        +to_list_dict() List
    }

    class Animal {
        <<abstract>>
        -_nome: str
        -_raca: str
        -_status: StatusAnimal
        -_porte: PorteAnimal
        -_temperamento: List
        +historico_eventos: List
        +data_reserva: str
        +nome_reservante: str
        +fila_espera: FilaEspera
        +__init__(nome, raca, status, porte, temp)
        +nome() str
        +status() StatusAnimal
        +porte() PorteAnimal
        +temperamento() List
        +adicionar_evento(descricao)
        +pode_mudar_para(novo_status) bool
        +mudar_status(novo_status)
        +to_dict()* Dict
        +from_dict(dados)* Animal$
    }

    class Cachorro {
        -_precisa_passeio: bool
        +__init__(...)
        +to_dict() Dict
        +from_dict_concreto(dados) Cachorro$
        +__str__() str
    }

    class Gato {
        -_independencia: int
        +__init__(...)
        +to_dict() Dict
        +from_dict_concreto(dados) Gato$
        +__str__() str
    }

    %% Relacionamentos de Domínio
    Animal <|-- Cachorro
    Animal <|-- Gato
    VacinavelMixin <|-- Cachorro
    VacinavelMixin <|-- Gato
    AdestravelMixin <|-- Cachorro
    Animal *-- FilaEspera
    Animal ..> StatusAnimal
    Animal ..> PorteAnimal
    Adotante ..> TipoMoradia

    %% --- REPOSITORIES ---
    class Repositorio {
        <<interface>>
        +salvar_animais(animais)
        +carregar_animais() List
        +salvar_adotantes(adotantes)
        +carregar_adotantes() List
    }

    class RepositorioJSON {
        +arquivo_animais: str
        +arquivo_adotantes: str
        +__init__()
        +salvar_animais(animais)
        +carregar_animais() List
        +salvar_adotantes(adotantes)
        +carregar_adotantes() List
    }

    class RepositorioSQLite {
        +db_name: str
        +__init__()
        -_get_conexao() Connection
        -_inicializar_banco()
        +salvar_animais(animais)
        +carregar_animais() List
        +salvar_adotantes(adotantes)
        +carregar_adotantes() List
    }

    Repositorio <|.. RepositorioJSON
    Repositorio <|.. RepositorioSQLite

    %% --- STRATEGY (TAXAS) ---
    class EstrategiaTaxa {
        <<interface>>
        +calcular(animal, adotante) str
    }

    class TaxaPadrao {
        +calcular(animal, adotante) str
    }
    class TaxaSenior {
        +calcular(animal, adotante) str
    }
    class TaxaPorteGrande {
        +calcular(animal, adotante) str
    }

    class FabricaTaxas {
        +obter_estrategia(animal, adotante) EstrategiaTaxa$
    }

    EstrategiaTaxa <|.. TaxaPadrao
    EstrategiaTaxa <|.. TaxaSenior
    EstrategiaTaxa <|.. TaxaPorteGrande
    FabricaTaxas ..> EstrategiaTaxa : cria

    %% --- OBSERVER ---
    class Observador {
        <<interface>>
        +atualizar(mensagem)
    }

    class LoggerObserver {
        +arquivo: str
        +__init__(arquivo)
        +atualizar(mensagem)
    }

    Observador <|.. LoggerObserver

    %% --- FACADE (SISTEMA) ---
    class SistemaAdocao {
        +settings: Dict
        +animais: List
        +adotantes: List
        +repo: Repositorio
        +observadores: List
        +__init__()
        +adicionar_observador(observador)
        +notificar_observadores(evento)
        -_carregar_settings() Dict
        -_salvar_settings_arquivo(dados)
        +atualizar_configuracao(chave, valor)
        +buscar_animal(idx) Animal
        +buscar_adotante(idx) Adotante
        +cadastrar_cachorro(nome, raca, porte, temp, passeio)
        +cadastrar_gato(nome, raca, porte, temp, indep)
        +cadastrar_adotante(nome, contato, idade, moradia, area, kids)
        +excluir_animal(idx)
        +excluir_adotante(idx)
        +editar_animal(idx, ...)
        +editar_adotante(idx, ...)
        -_buscar_por_indice(idx_ani, idx_ado)
        -_validar_politica_adocao(animal, adotante)
        -_calcular_compatibilidade(animal, adotante)
        +reservar_animal(idx_ani, idx_ado)
        +realizar_adocao(idx_ani, idx_ado)
        +processar_devolucao(idx_ani, motivo)
        +entrar_fila_espera(idx_ani, idx_ado)
        +processar_reservas_vencidas()
        +visualizar_detalhes_fila(idx_ani)
        +vacinar_animal(idx_ani, vacina)
        +treinar_animal(idx_ani)
        +gerar_relatorio_animais(apenas_adotados)
        +listar_adotantes()
        +gerar_relatorios_estatisticos()
        -_calcular_taxa_adocao_por_tipo(classe)
        -_calcular_tempo_medio_adocao()
    }

    SistemaAdocao --> Repositorio : usa
    SistemaAdocao --> Observador : notifica
    SistemaAdocao ..> FabricaTaxas : usa
    SistemaAdocao "1" o-- "*" Animal : gerencia
    SistemaAdocao "1" o-- "*" Adotante : gerencia

```
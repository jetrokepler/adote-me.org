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



### 🧪 Executando os Testes

Todos os testes são feitos com **Pytest**:

```bash
pytest
```

Com relatório mais detalhado:

```bash
pytest -v
```

---

# 🏛️ Arquitetura


```mermaid
classDiagram

    %% ENUMS
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

    %% MIXINS
    class VacinavelMixin {
        agenda_vacinas
        vacinar()
    }

    class AdestravelMixin {
        nivel_adestramento
        treinar()
    }

    %% PESSOAS
    class Pessoa {
        <<abstract>>
        nome
        contato
    }

    class Adotante {
        idade
        moradia
        area_util
        tem_criancas
        to_dict()
        from_dict()
    }

    Pessoa <|-- Adotante

    %% ANIMAIS
    class FilaEspera {
        interessados
        adicionar()
        proximo()
    }

    class Animal {
        <<abstract>>
        nome
        raca
        status
        porte
        temperamento
        adicionar_evento()
        mudar_status()
    }

    class Cachorro {
        precisa_passeio
    }

    class Gato {
        independencia
    }

    Animal <|-- Cachorro
    Animal <|-- Gato
    Animal *-- FilaEspera

    %% REPOSITORY
    class Repositorio {
        <<interface>>
        salvar_animais()
        carregar_animais()
        salvar_adotantes()
        carregar_adotantes()
    }

    class RepositorioJSON
    class RepositorioSQLite

    Repositorio <|.. RepositorioJSON
    Repositorio <|.. RepositorioSQLite

    %% STRATEGY
    class EstrategiaTaxa {
        <<interface>>
        calcular()
    }

    class TaxaPadrao
    class TaxaSenior
    class TaxaPorteGrande

    EstrategiaTaxa <|.. TaxaPadrao
    EstrategiaTaxa <|.. TaxaSenior
    EstrategiaTaxa <|.. TaxaPorteGrande

    %% OBSERVER
    class Observador {
        <<interface>>
        atualizar()
    }

    class LoggerObserver

    Observador <|.. LoggerObserver

    %% SISTEMA
    class SistemaAdocao {
        animais
        adotantes
        reservar_animal()
        realizar_adocao()
        gerar_relatorios()
    }

    SistemaAdocao --> Repositorio
    SistemaAdocao --> Observador
```

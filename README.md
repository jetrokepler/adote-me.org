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

### Tipos e Pessoas

| Classe / Tipo | Descrição e Estrutura |
| :--- | :--- |
| **Tipos Básicos**<br>*(Enums)* | **`StatusAnimal`**: DISPONIVEL, RESERVADO, ADOTADO<br>**`PorteAnimal`**: P (Pequeno), M (Médio), G (Grande)<br>**`TipoMoradia`**: CASA, APTO |
| **Pessoa**<br>*(Classe Abstrata)* | **Atributos Base:**<br>• `nome`: Texto<br>• `contato`: Texto |
| **Adotante**<br>*(Herda de Pessoa)* | **Atributos:**<br>• `moradia`: TipoMoradia<br>• `tem_criancas`: Booleano<br>**Métodos:**<br>• `eh_compativel(animal)`: Verifica regras de porte vs. moradia. |

### Animais (Hierarquia)

| Classe | Detalhes |
| :--- | :--- |
| **Animal**<br>*(Classe Abstrata)* | **Atributos:**<br>• `nome`: Texto<br>• `status`: StatusAnimal<br>• `porte`: PorteAnimal<br>**Métodos:**<br>• `mudar_status(novo_status)` |
| **Cachorro**<br>*(Herda de Animal)* | **Específico:**<br>• `precisa_passeio`: Booleano |
| **Gato**<br>*(Herda de Animal)* | **Específico:**<br>• `independencia`: Número (Nível 0-5) |

### Núcleo do Sistema e Auxiliares

| Componente | Responsabilidade |
| :--- | :--- |
| **SistemaAdocao**<br>*(Gerente Geral)* | **Atributos:**<br>• `repositorio`: Repositorio<br>• `calculadora`: CalculadoraTaxas<br>• `animais`: Lista<br>**Métodos Principais:**<br>• `cadastrar_animal()`<br>• `reservar_animal()`<br>• `efetivar_adocao()` |
| **Repositorio**<br>*(Persistência)* | **Função:** Salvar e carregar dados (JSON).<br>**Métodos:**<br>• `salvar(dados)`<br>• `carregar()` |
| **CalculadoraTaxas**<br>*(Lógica)* | **Função:** Definir o valor da adoção.<br>**Métodos:**<br>• `calcular_preco(animal)` |

### Transações (Ações)

| Classe | Estrutura |
| :--- | :--- |
| **Reserva** | **Conecta:** `Animal` + `Adotante`<br>**Atributos:**<br>• `data_validade`: Data<br>**Métodos:**<br>• `esta_vencida()` |
| **Adocao** | **Registro Final**<br>**Atributos:**<br>• `animal`: Animal<br>• `adotante`: Adotante<br>• `valor_pago`: Valor<br>• `data`: Data<br>**Métodos:**<br>• `gerar_recibo()` |
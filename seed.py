import sys
import os

# Garante que o Python encontre o pacote src
sys.path.append(os.getcwd())

try:
    from src.adocao.services import SistemaAdocao
    from src.adocao.enums import PorteAnimal, TipoMoradia
except ImportError as e:
    print("❌ Erro de importação: Execute este arquivo da RAIZ do projeto.")
    print(f"Detalhe: {e}")
    sys.exit(1)

def popular_banco():
    # Limpeza inicial
    if os.path.exists("animais.json"): os.remove("animais.json")
    if os.path.exists("adotantes.json"): os.remove("adotantes.json")
    
    sistema = SistemaAdocao()
    print("🚀 Iniciando Seed com Scores Variados...")

    # ==============================================================================
    # 1. CADASTRO DE ANIMAIS (30 Animais)
    # ==============================================================================
    print("🐱 Cadastrando Gatos...")
    gatos = [
        # Nome, Raça, Porte, Temperamento, Independência
        ("Simba", "SRD Laranja", PorteAnimal.M, ["amoroso", "calmo"], 3),       # 0
        ("Luna", "Siamês", PorteAnimal.P, ["vocal", "pegajoso"], 1),            # 1
        ("Thor", "Maine Coon", PorteAnimal.G, ["gigante", "dócil"], 5),         # 2 (FILA GIGANTE)
        ("Salem", "Bombaim", PorteAnimal.M, ["independente"], 9),               # 3
        ("Garfield", "Persa", PorteAnimal.M, ["preguiçoso"], 2),                # 4
        ("Frajola", "SRD", PorteAnimal.M, ["brincalhão"], 6),                   # 5
        ("Nala", "Angorá", PorteAnimal.P, ["arisco", "nervoso"], 8),            # 6 
        ("Tom", "Russian Blue", PorteAnimal.M, ["inteligente"], 7),             # 7
        ("Marie", "Branquelo", PorteAnimal.P, ["mimada"], 2),                   # 8
        ("Chico", "Tigrado", PorteAnimal.G, ["territorial"], 6),                # 9
        ("Mittens", "Ragdoll", PorteAnimal.G, ["muito dócil"], 1),              # 10
        ("Zelda", "Sphynx", PorteAnimal.P, ["carente"], 0),                     # 11
        ("Loki", "Bengal", PorteAnimal.M, ["destruidor", "ativo"], 10),         # 12
        ("Pantera", "SRD Preto", PorteAnimal.G, ["protetor"], 5),               # 13
        ("Mochi", "Munchkin", PorteAnimal.P, ["fofo"], 4),                      # 14
    ]
    for n, r, p, t, i in gatos: sistema.cadastrar_gato(n, r, p, t, i)

    print("🐶 Cadastrando Cães...")
    caes = [
        # Nome, Raça, Porte, Temperamento, Passeio
        ("Rex", "Pastor Alemão", PorteAnimal.G, ["protetor"], True),            # 15
        ("Mel", "Golden", PorteAnimal.G, ["amoroso", "amigo"], True),           # 16 (FILA)
        ("Pipoca", "Pinscher", PorteAnimal.P, ["agressivo"], False),            # 17
        ("Paçoca", "Vira-lata", PorteAnimal.M, ["feliz"], True),                # 18
        ("Zeus", "Husky", PorteAnimal.G, ["agitado"], True),                    # 19
        ("Lulu", "Poodle", PorteAnimal.P, ["elegante"], False),                 # 20
        ("Brutos", "Pitbull", PorteAnimal.G, ["dócil"], True),                  # 21
        ("Salsicha", "Dachshund", PorteAnimal.P, ["teimoso"], False),           # 22
        ("Scooby", "Dogue Alemão", PorteAnimal.G, ["medroso"], True),           # 23
        ("Totó", "SRD", PorteAnimal.M, ["leal"], False),                        # 24
    ]
    for n, r, p, t, pass_ in caes: sistema.cadastrar_cachorro(n, r, p, t, pass_)

    # ==============================================================================
    # 2. CADASTRO DE ADOTANTES (Mix de Idades para variar Score)
    # Lógica do Sistema: > 30 anos ganha +20 pts de experiência
    # ==============================================================================
    print("\n👤 Cadastrando Adotantes (Jovens vs Experientes)...")
    adotantes = [
        # Nome, Email, Idade, Moradia, Area, Tem Crianças
        # JOVENS (Score base menor - 80)
        ("Ana Souza", "ana@x.com", 22, TipoMoradia.APTO, 60.0, False),          # 0 (Jovem Apto)
        ("Fernanda", "fe@x.com", 22, TipoMoradia.APTO, 45.0, False),            # 1 (Jovem Apto)
        ("Gabriel", "gabi@x.com", 29, TipoMoradia.CASA, 80.0, False),           # 2 (Jovem Casa)
        ("Julia", "ju@x.com", 19, TipoMoradia.APTO, 50.0, False),               # 3 (Jovem Apto)
        ("Natalia", "nat@x.com", 27, TipoMoradia.APTO, 70.0, False),            # 4 (Jovem Apto)
        ("Rafael", "rafa@x.com", 24, TipoMoradia.APTO, 55.0, False),            # 5 (Jovem Apto)
        ("Tiago", "ti@x.com", 28, TipoMoradia.CASA, 80.0, False),               # 6 (Jovem Casa)
        
        # EXPERIENTES (Score base maior - 100)
        ("Beto Lima", "beto@x.com", 45, TipoMoradia.CASA, 200.0, True),         # 7 (Exp Casa)
        ("Dona Bento", "bento@x.com", 70, TipoMoradia.CASA, 150.0, False),      # 8 (Senior Casa)
        ("Eduardo", "edu@x.com", 35, TipoMoradia.CASA, 500.0, False),           # 9 (Exp Casa)
        ("Helena", "he@x.com", 40, TipoMoradia.CASA, 300.0, True),              # 10 (Exp Casa)
        ("Igor", "igor@x.com", 50, TipoMoradia.CASA, 120.0, False),             # 11 (Exp Casa)
        ("Kleber", "kleber@x.com", 60, TipoMoradia.CASA, 250.0, False),         # 12 (Exp Casa)
        ("Laura", "laura@x.com", 33, TipoMoradia.CASA, 100.0, True),            # 13 (Exp Casa)
        ("Marcos", "marc@x.com", 44, TipoMoradia.CASA, 180.0, False),           # 14 (Exp Casa)
        ("Otavio", "ota@x.com", 38, TipoMoradia.CASA, 90.0, True),              # 15 (Exp Casa)
        ("Paula", "pau@x.com", 31, TipoMoradia.CASA, 110.0, False),             # 16 (Exp Casa)
        ("Quintino", "quin@x.com", 55, TipoMoradia.CASA, 200.0, False),         # 17 (Exp Casa)
        ("Sandra", "san@x.com", 45, TipoMoradia.CASA, 150.0, True),             # 18 (Exp Casa)
        ("Carla Dias", "carla@x.com", 35, TipoMoradia.APTO, 100.0, True),       # 19 (Exp Apto)
    ]
    for dados in adotantes: sistema.cadastrar_adotante(*dados)

    # ==============================================================================
    # 3. CENÁRIOS E OPERAÇÕES
    # ==============================================================================
    print("\n🎬 Executando Cenários...")

    # --- ADOÇÕES ---
    print(" -> Realizando Adoções...")
    sistema.realizar_adocao(0, 0)   # Ana (Jovem) adota Simba
    sistema.realizar_adocao(8, 8)   # Dona Bento (Senior) adota Marie
    sistema.realizar_adocao(1, 1)   # Fernanda adota Luna
    sistema.realizar_adocao(9, 13)  # Eduardo adota Pantera (Gato G)
    sistema.realizar_adocao(15, 12) # Otavio adota Rex (Cão G)
    sistema.realizar_adocao(4, 20)  # Natalia adota Lulu

    # --- DEVOLUÇÕES ---
    print(" -> Processando Devoluções...")
    
    # Devolução por Saúde
    sistema.realizar_adocao(12, 3) # Julia adota Loki (M)
    sistema.processar_devolucao(12, "Doença grave detectada")

    # Devolução por Agressividade
    sistema.realizar_adocao(17, 6) # Tiago adota Pipoca (P)
    sistema.processar_devolucao(17, "Ele atacou minha visita (agressivo)")

    # Devolução Normal
    sistema.realizar_adocao(18, 5) # Rafael adota Paçoca
    sistema.processar_devolucao(18, "Motivos financeiros")

    # --- FILA DE ESPERA COM SCORE VARIADO ---
    print(" -> Criando Filas com Pontuações Diferentes...")
    
    # ANIMAL: THOR (Maine Coon - Porte G - Exige Casa)
    # Reserva inicial: Beto (ID 7)
    sistema.reservar_animal(2, 7)
    
    print("   [Fila Thor] Inserindo misto de Jovens (<30 anos) e Experientes (>30 anos)...")
    
    # Tiago (ID 6): 28 anos -> Score deve ser ~80 (Perde pts de experiência)
    sistema.entrar_fila_espera(2, 6)
    
    # Quintino (ID 17): 55 anos -> Score deve ser 100 (Experiência ok)
    sistema.entrar_fila_espera(2, 17)
    
    # Gabriel (ID 2): 29 anos -> Score deve ser ~80
    sistema.entrar_fila_espera(2, 2)
    
    # Paula (ID 16): 31 anos -> Score deve ser 100
    sistema.entrar_fila_espera(2, 16)

    # ANIMAL: MEL (Golden - Porte G - Exige Casa)
    # Reserva inicial: Helena (ID 10)
    sistema.reservar_animal(16, 10)
    
    print("   [Fila Mel] Inserindo mais candidatos...")
    
    # Laura (ID 13): 33 anos (Score 100)
    sistema.entrar_fila_espera(16, 13)
    
    # Sandra (ID 18): 45 anos (Score 100)
    sistema.entrar_fila_espera(16, 18)

    print("\n✅ SEED FINALIZADO!")
    print(f"📊 Verifique o relatório (Opção 14) ou Detalhes da Fila (Opção 12)")
    print(f"   - IDs para checar fila: 2 (Thor) e 16 (Mel)")

if __name__ == "__main__":
    popular_banco()
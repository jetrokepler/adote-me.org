import sys
import os
import json

sys.path.append(os.getcwd())

try:
    from src.adocao.services import SistemaAdocao
    from src.adocao.enums import PorteAnimal, TipoMoradia
except ImportError as e:
    print("❌ Erro de importação: Execute este arquivo da RAIZ do projeto.")
    print(f"Detalhe: {e}")
    sys.exit(1)

def popular_banco():
    modo_sqlite = False
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                if dados.get("banco_tipo") == "SQLITE":
                    modo_sqlite = True
        except:
            pass

    if modo_sqlite:
        if os.path.exists("adocao.db"):
            os.remove("adocao.db")
            print("🧹 Banco de dados SQLite limpo.")
    else:
        if os.path.exists("animais.json"): os.remove("animais.json")
        if os.path.exists("adotantes.json"): os.remove("adotantes.json")
        print("🧹 Arquivos JSON limpos.")
    
    sistema = SistemaAdocao()
    print(f"🚀 Iniciando Seed ({'SQLite' if modo_sqlite else 'JSON'})...")

    print("🐱 Cadastrando Gatos...")
    gatos = [
        ("Simba", "SRD Laranja", PorteAnimal.M, ["amoroso", "calmo"], 3),
        ("Luna", "Siamês", PorteAnimal.P, ["vocal", "pegajoso"], 1),
        ("Thor", "Maine Coon", PorteAnimal.G, ["gigante", "dócil"], 5),
        ("Salem", "Bombaim", PorteAnimal.M, ["independente"], 9),
        ("Garfield", "Persa", PorteAnimal.M, ["preguiçoso"], 2),
        ("Frajola", "SRD", PorteAnimal.M, ["brincalhão"], 6),
        ("Nala", "Angorá", PorteAnimal.P, ["arisco", "nervoso"], 8), 
        ("Tom", "Russian Blue", PorteAnimal.M, ["inteligente"], 7),
        ("Marie", "Branquelo", PorteAnimal.P, ["mimada"], 2),
        ("Chico", "Tigrado", PorteAnimal.G, ["territorial"], 6),
        ("Mittens", "Ragdoll", PorteAnimal.G, ["muito dócil"], 1),
        ("Zelda", "Sphynx", PorteAnimal.P, ["carente"], 0),
        ("Loki", "Bengal", PorteAnimal.M, ["destruidor", "ativo"], 10),
        ("Pantera", "SRD Preto", PorteAnimal.G, ["protetor"], 5),
        ("Mochi", "Munchkin", PorteAnimal.P, ["fofo"], 4),
    ]
    for n, r, p, t, i in gatos: sistema.cadastrar_gato(n, r, p, t, i)

    print("🐶 Cadastrando Cães...")
    caes = [
        ("Rex", "Pastor Alemão", PorteAnimal.G, ["protetor"], True),
        ("Mel", "Golden", PorteAnimal.G, ["amoroso", "amigo"], True),
        ("Pipoca", "Pinscher", PorteAnimal.P, ["agressivo"], False),
        ("Paçoca", "Vira-lata", PorteAnimal.M, ["feliz"], True),
        ("Zeus", "Husky", PorteAnimal.G, ["agitado"], True),
        ("Lulu", "Poodle", PorteAnimal.P, ["elegante"], False),
        ("Brutos", "Pitbull", PorteAnimal.G, ["dócil"], True),
        ("Salsicha", "Dachshund", PorteAnimal.P, ["teimoso"], False),
        ("Scooby", "Dogue Alemão", PorteAnimal.G, ["medroso"], True),
        ("Totó", "SRD", PorteAnimal.M, ["leal"], False),
    ]
    for n, r, p, t, pass_ in caes: sistema.cadastrar_cachorro(n, r, p, t, pass_)

    print("\n👤 Cadastrando Adotantes (Jovens vs Experientes)...")
    adotantes = [
        ("Ana Souza", "ana@x.com", 22, TipoMoradia.APTO, 60.0, False),
        ("Fernanda", "fe@x.com", 22, TipoMoradia.APTO, 45.0, False),
        ("Gabriel", "gabi@x.com", 29, TipoMoradia.CASA, 80.0, False),
        ("Julia", "ju@x.com", 19, TipoMoradia.APTO, 50.0, False),
        ("Natalia", "nat@x.com", 27, TipoMoradia.APTO, 70.0, False),
        ("Rafael", "rafa@x.com", 24, TipoMoradia.APTO, 55.0, False),
        ("Tiago", "ti@x.com", 28, TipoMoradia.CASA, 80.0, False),
        
        ("Beto Lima", "beto@x.com", 45, TipoMoradia.CASA, 200.0, True),
        ("Dona Bento", "bento@x.com", 70, TipoMoradia.CASA, 150.0, False),
        ("Eduardo", "edu@x.com", 35, TipoMoradia.CASA, 500.0, False),
        ("Helena", "he@x.com", 40, TipoMoradia.CASA, 300.0, True),
        ("Igor", "igor@x.com", 50, TipoMoradia.CASA, 120.0, False),
        ("Kleber", "kleber@x.com", 60, TipoMoradia.CASA, 250.0, False),
        ("Laura", "laura@x.com", 33, TipoMoradia.CASA, 100.0, True),
        ("Marcos", "marc@x.com", 44, TipoMoradia.CASA, 180.0, False),
        ("Otavio", "ota@x.com", 38, TipoMoradia.CASA, 90.0, True),
        ("Paula", "pau@x.com", 31, TipoMoradia.CASA, 110.0, False),
        ("Quintino", "quin@x.com", 55, TipoMoradia.CASA, 200.0, False),
        ("Sandra", "san@x.com", 45, TipoMoradia.CASA, 150.0, True),
        ("Carla Dias", "carla@x.com", 35, TipoMoradia.APTO, 100.0, True),
    ]
    for dados in adotantes: sistema.cadastrar_adotante(*dados)

    print("\n🎬 Executando Cenários...")

    print(" -> Realizando Adoções...")
    sistema.realizar_adocao(0, 0)
    sistema.realizar_adocao(8, 8)
    sistema.realizar_adocao(1, 1)
    sistema.realizar_adocao(9, 13)
    sistema.realizar_adocao(15, 12)
    sistema.realizar_adocao(4, 20)

    print(" -> Processando Devoluções...")
    
    sistema.realizar_adocao(12, 3)
    sistema.processar_devolucao(12, "Doença grave detectada")

    sistema.realizar_adocao(17, 6)
    sistema.processar_devolucao(17, "Ele atacou minha visita (agressivo)")

    sistema.realizar_adocao(18, 5)
    sistema.processar_devolucao(18, "Motivos financeiros")

    print(" -> Criando Filas com Pontuações Diferentes...")
    
    sistema.reservar_animal(2, 7)
    
    print("   [Fila Thor] Inserindo misto de Jovens (<30 anos) e Experientes (>30 anos)...")
    
    sistema.entrar_fila_espera(2, 6)
    
    sistema.entrar_fila_espera(2, 17)
    
    sistema.entrar_fila_espera(2, 2)
    
    sistema.entrar_fila_espera(2, 16)

    sistema.reservar_animal(16, 10)
    
    print("   [Fila Mel] Inserindo mais candidatos...")
    
    sistema.entrar_fila_espera(16, 13)
    
    sistema.entrar_fila_espera(16, 18)

    print("\n✅ SEED FINALIZADO!")
    print(f"📊 Verifique o relatório (Opção 14) ou Detalhes da Fila (Opção 12)")
    print(f"   - IDs para checar fila: 2 (Thor) e 16 (Mel)")

if __name__ == "__main__":
    popular_banco()
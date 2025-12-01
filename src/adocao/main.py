from .services import SistemaAdocao
from .enums import PorteAnimal, TipoMoradia

def main():
    sistema = SistemaAdocao()

    while True:
        # Gradiente estilo neofetch (ciano → azul → roxo → rosa)
        G1 = "\033[38;2;0;255;255m"   # Cyan
        G2 = "\033[38;2;0;170;255m"   # Blue
        G3 = "\033[38;2;170;0;255m"   # Purple
        G4 = "\033[38;2;255;0;150m"   # Pink
        RESET = "\033[0m"

        print(rf"""
        (\__/)
        ( •ᴥ•)
        / >🎀   [ {G1}a{G2}d{G3}o{G4}t{G1}e{G2}-{G3}m{G4}e{G1}.{G2}o{G3}r{G4}g{RESET} ]
        """)
        print("\n=== 🐾 adote-me.org ===")
        print("1. Cadastrar Cachorro")
        print("2. Cadastrar Gato")
        print("3. Cadastrar Adotante")
        print("4. Relatório (Disponíveis/Adotados)")
        print("5. Realizar Adoção (Vincular Adotante a Animal)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- Novo Cachorro ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            p = input("Escolha: ")
            porte = PorteAnimal.P if p == "1" else PorteAnimal.M if p == "2" else PorteAnimal.G
            passeio = input("Precisa de muito passeio? (s/n): ").lower() == 's'
            sistema.cadastrar_cachorro(nome, raca, porte, passeio)

        elif opcao == "2":
            print("\n--- Novo Gato ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            p = input("Escolha: ")
            indep = int(input("Nível de independência (0 a 5): "))
            sistema.cadastrar_gato(nome, raca, PorteAnimal.P, indep)

        elif opcao == "3":
            print("\n--- Novo Adotante ---")
            nome = input("Nome: ")
            contato = input("Contato: ")
            print("Moradia: 1-Casa, 2-Apto")
            m = input("Escolha: ")
            moradia = TipoMoradia.CASA if m == "1" else TipoMoradia.APTO
            criancas = input("Tem crianças em casa? (s/n): ").lower() == 's'
            sistema.cadastrar_adotante(nome, contato, moradia, criancas)

        elif opcao == "4":
            sistema.gerar_relatorio_animais()

        elif opcao == "5":
            sistema.listar_indices()
            try:
                id_animal = int(input("\nDigite o ID (número) do Animal: "))
                id_adotante = int(input("Digite o ID (número) do Adotante: "))
                sistema.realizar_adocao_simples(id_animal, id_adotante)
            except ValueError:
                print("❌ Por favor, digite apenas números.")

        elif opcao == "0":
            print("Saindo... Seus dados estão salvos! 💾")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
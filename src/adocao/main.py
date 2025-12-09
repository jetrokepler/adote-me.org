from .services import SistemaAdocao
from .enums import PorteAnimal, TipoMoradia

def main():
    sistema = SistemaAdocao()

    while True:
        
        G1 = "\033[38;2;0;255;255m"   
        G2 = "\033[38;2;0;170;255m"   
        G3 = "\033[38;2;170;0;255m"   
        G4 = "\033[38;2;255;0;150m"   
        RESET = "\033[0m"

        print(rf"""
        (\__/)
        ( •ᴥ•)
        / >🎀   [ {G1}a{G2}d{G3}o{G4}t{G1}e{G2}-{G3}m{G4}e{G1}.{G2}o{G3}r{G4}g{RESET} ]
        """)
        print(f"\n=== 🐾 {G1}ADOTE-ME.ORG{RESET} ===")
        print("1. Cadastrar Cachorro")
        print("2. Cadastrar Gato")
        print("3. Cadastrar Adotante")
        print("4. Relatório (Listar Tudo)")
        print("5. RESERVAR Animal")
        print("6. ADOTAR Animal")
        print("7. DEVOLVER Animal")
        print("0. Sair")
        
        opcao = input(f"\n{G3}Escolha uma opção:{RESET} ")

        if opcao == "1":
            print(f"\n--- {G1}Novo Cachorro{RESET} ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            p = input("Escolha: ")
            porte = PorteAnimal.G if p == "3" else PorteAnimal.M if p == "2" else PorteAnimal.P
            
            # --- INPUT NOVO DA SEMANA 4 ---
            temp_str = input("Temperamento (ex: calmo,arisco): ")
            temperamento = [t.strip() for t in temp_str.split(",")]
            
            passeio = input("Precisa de muito passeio? (s/n): ").lower() == 's'
            sistema.cadastrar_cachorro(nome, raca, porte, temperamento, passeio)

        elif opcao == "2":
            print(f"\n--- {G1}Novo Gato{RESET} ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            p = input("Escolha: ")
            porte = PorteAnimal.G if p == "3" else PorteAnimal.M if p == "2" else PorteAnimal.P

            temp_str = input("Temperamento (ex: calmo,arisco): ")
            temperamento = [t.strip() for t in temp_str.split(",")]

            indep = int(input("Nível de independência (0 a 5): "))
            sistema.cadastrar_gato(nome, raca, porte, temperamento, indep)

        elif opcao == "3":
            print(f"\n--- {G1}Novo Adotante{RESET} ---")
            nome = input("Nome: ")
            contato = input("Contato: ")
            
            idade = int(input("Idade: "))
            
            print("Moradia: 1-Casa, 2-Apto")
            m = input("Escolha: ")
            moradia = TipoMoradia.CASA if m == "1" else TipoMoradia.APTO
            
            area = float(input("Área útil (m²): "))
            criancas = input("Tem crianças em casa? (s/n): ").lower() == 's'
            
            sistema.cadastrar_adotante(nome, contato, idade, moradia, area, criancas)

        elif opcao == "4":
            sistema.gerar_relatorio_animais()
            sistema.listar_adotantes()

        elif opcao == "5":
            print(f"\n--- {G2}Reservar Animal{RESET} ---")
            try:
                id_animal = int(input("ID Animal: "))
                id_adotante = int(input("ID Adotante: "))
                sistema.reservar_animal(id_animal, id_adotante)
            except ValueError:
                print("❌ Digite apenas números.")

        elif opcao == "6":
            print(f"\n--- {G4}Realizar Adoção{RESET} ---")
            try:
                id_animal = int(input("ID Animal: "))
                id_adotante = int(input("ID Adotante: "))
  
                sistema.realizar_adocao(id_animal, id_adotante)
            except ValueError:
                print("❌ Digite apenas números.")

        elif opcao == "7": 
            print(f"\n--- {G3}Devolução{RESET} ---")
            try:
                id_animal = int(input("ID Animal: "))
                motivo = input("Motivo da devolução: ")
                sistema.processar_devolucao(id_animal, motivo)
            except ValueError:
                print("❌ Digite apenas números.")

        elif opcao == "0":
            print(f"\n{G4}Saindo... Seus dados estão salvos! 💾{RESET}")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
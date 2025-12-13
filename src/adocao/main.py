from .services import SistemaAdocao
from .enums import PorteAnimal, TipoMoradia
from .domain import Cachorro, Gato

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
        print("-" * 25)
        print("8. ✏️  EDITAR Animal")
        print("9. 🗑️  EXCLUIR Animal")
        print("10. ✏️  EDITAR Adotante")
        print("11. 🗑️  EXCLUIR Adotante")
        print("-" * 25)
        print("0. Sair")
        
        opcao = input(f"\n{G3}Escolha uma opção:{RESET} ")

        if opcao == "1":
            print(f"\n--- {G1}Novo Cachorro{RESET} ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            p = input("Escolha: ")
            porte = PorteAnimal.G if p == "3" else PorteAnimal.M if p == "2" else PorteAnimal.P
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
            except ValueError: print("❌ Digite apenas números.")

        elif opcao == "6":
            print(f"\n--- {G4}Realizar Adoção{RESET} ---")
            try:
                id_animal = int(input("ID Animal: "))
                id_adotante = int(input("ID Adotante: "))
                sistema.realizar_adocao(id_animal, id_adotante)
            except ValueError: print("❌ Digite apenas números.")

        elif opcao == "7":
            print(f"\n--- {G3}Devolução{RESET} ---")
            try:
                id_animal = int(input("ID Animal: "))
                motivo = input("Motivo da devolução: ")
                sistema.processar_devolucao(id_animal, motivo)
            except ValueError: print("❌ Digite apenas números.")


        elif opcao == "8":
            sistema.gerar_relatorio_animais()
            try:
                idx = int(input("\nID do Animal para editar: "))
                print(f"{G2}[Deixe vazio e aperte Enter para não alterar]{RESET}")
                
                nome = input("Novo Nome: ").strip() or None
                raca = input("Nova Raça: ").strip() or None
                
                p_in = input("Novo Porte (1-P, 2-M, 3-G): ").strip()
                porte = None
                if p_in == "1": porte = PorteAnimal.P
                elif p_in == "2": porte = PorteAnimal.M
                elif p_in == "3": porte = PorteAnimal.G

                temp_str = input("Novo Temperamento (sep. virgula): ").strip()
                temperamento = [t.strip() for t in temp_str.split(",")] if temp_str else None

                extra = None
                if 0 <= idx < len(sistema.animais):
                    animal_atual = sistema.animais[idx]
                    if isinstance(animal_atual, Cachorro):
                        p_str = input("Precisa Passeio? (s/n): ").strip().lower()
                        extra = True if p_str == 's' else False if p_str == 'n' else None
                    elif isinstance(animal_atual, Gato):
                        ind_str = input("Nível Indep (0-5): ").strip()
                        extra = int(ind_str) if ind_str else None

                sistema.editar_animal(idx, nome, raca, porte, temperamento, extra)
            except ValueError: print("❌ Erro de valor.")

        elif opcao == "9": 
            sistema.gerar_relatorio_animais()
            try:
                idx = int(input("\nID do Animal para EXCLUIR: "))
                confirmacao = input("Tem certeza? (s/n): ").lower()
                if confirmacao == 's':
                    sistema.excluir_animal(idx)
            except ValueError: print("❌ Erro numérico.")

        elif opcao == "10": 
            sistema.listar_adotantes()
            try:
                idx = int(input("\nID do Adotante para editar: "))
                print(f"{G2}[Deixe vazio e aperte Enter para não alterar]{RESET}")

                nome = input("Novo Nome: ").strip() or None
                contato = input("Novo Contato: ").strip() or None
                
                m_in = input("Nova Moradia (1-Casa, 2-Apto): ").strip()
                moradia = TipoMoradia.CASA if m_in == "1" else TipoMoradia.APTO if m_in == "2" else None

                area_str = input("Nova Área útil: ").strip()
                area = float(area_str) if area_str else None

                sistema.editar_adotante(idx, nome, contato, moradia, area)
            except ValueError: print("❌ Erro de valor.")

        elif opcao == "11":
            sistema.listar_adotantes()
            try:
                idx = int(input("\nID do Adotante para EXCLUIR: "))
                confirmacao = input("Tem certeza? (s/n): ").lower()
                if confirmacao == 's':
                    sistema.excluir_adotante(idx)
            except ValueError: print("❌ Erro numérico.")

        elif opcao == "0":
            print(f"\n{G4}Saindo... Seus dados estão salvos! 💾{RESET}")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
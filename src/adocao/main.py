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
        print(f"\n=== 🐾 {G1}MENU PRINCIPAL{RESET} ===")
        print("1. Cadastrar Cachorro")
        print("2. Cadastrar Gato")
        print("3. Cadastrar Adotante")
        print("4. Relatório (Listar Tudo)")
        print("-" * 25)
        print("5. RESERVAR Animal")
        print("6. ADOTAR Animal")
        print("7. DEVOLVER Animal")
        print("-" * 25)
        print("8. ✏️  EDITAR Animal")
        print("9. 🗑️  EXCLUIR Animal")
        print("10. ✏️  EDITAR Adotante")
        print("11. 🗑️  EXCLUIR Adotante")
        print("-" * 25)
        print("12. 📊 VISUALIZAR Detalhes da Fila/Reserva")
        print("13. 🔄 Processar Reservas Vencidas")
        print("14. 📈 Gerar Relatórios Consolidados")
        print("-" * 25)
        print("0. Sair")
        
        opcao = input(f"\n{G3}Escolha uma opção:{RESET} ")

        if opcao == "1":
            print(f"\n--- {G1}Novo Cachorro{RESET} ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            escolha_porte = input("Escolha: ")
            porte = PorteAnimal.G if escolha_porte == "3" else PorteAnimal.M if escolha_porte == "2" else PorteAnimal.P
            
            print("Temperamento Principal:")
            print("1. Calmo/Dócil")
            print("2. Arisco/Agressivo")
            print("3. Outro (Digitar)")
            escolha_temp = input("Escolha: ")
            
            temperamento = []
            if escolha_temp == "1":
                temperamento = ["calmo"]
            elif escolha_temp == "2":
                temperamento = ["arisco"]
            else:
                temp_str = input("Digite o temperamento (ex: brincalhão): ")
                temperamento = [t.strip() for t in temp_str.split(",")]

            passeio_str = input("Precisa de muito passeio? (s/n): ").lower()
            precisa_passeio = (passeio_str == 's')
            
            sistema.cadastrar_cachorro(nome, raca, porte, temperamento, precisa_passeio)

        elif opcao == "2":
            print(f"\n--- {G1}Novo Gato{RESET} ---")
            nome = input("Nome: ")
            raca = input("Raça: ")
            
            print("Porte: 1-Pequeno, 2-Médio, 3-Grande")
            escolha_porte = input("Escolha: ")
            porte = PorteAnimal.G if escolha_porte == "3" else PorteAnimal.M if escolha_porte == "2" else PorteAnimal.P

            print("Temperamento Principal:")
            print("1. Calmo/Dócil")
            print("2. Arisco/Agressivo")
            print("3. Outro (Digitar)")
            escolha_temp = input("Escolha: ")
            
            temperamento = []
            if escolha_temp == "1":
                temperamento = ["calmo"]
            elif escolha_temp == "2":
                temperamento = ["arisco"]
            else:
                temp_str = input("Digite o temperamento: ")
                temperamento = [t.strip() for t in temp_str.split(",")]

            independencia = int(input("Nível de independência (0 a 5): "))
            sistema.cadastrar_gato(nome, raca, porte, temperamento, independencia)

        elif opcao == "3":
            print(f"\n--- {G1}Novo Adotante{RESET} ---")
            nome = input("Nome: ")
            contato = input("Contato: ")
            idade = int(input("Idade: "))
            
            print("Moradia: 1-Casa, 2-Apto")
            escolha_moradia = input("Escolha: ")
            moradia = TipoMoradia.CASA if escolha_moradia == "1" else TipoMoradia.APTO
            
            area_util = float(input("Área útil (m²): "))
            criancas_str = input("Tem crianças em casa? (s/n): ").lower()
            tem_criancas = (criancas_str == 's')
            
            sistema.cadastrar_adotante(nome, contato, idade, moradia, area_util, tem_criancas)

        elif opcao == "4":
            sistema.gerar_relatorio_animais()
            sistema.listar_adotantes()

        elif opcao == "5":
            print(f"\n--- {G2}Reservar Animal{RESET} ---")
            sistema.gerar_relatorio_animais()
            sistema.listar_adotantes()
            print("-" * 30)
            
            try:
                id_animal = int(input("Digite o ID do Animal: "))
                id_adotante = int(input("Digite o ID do Adotante: "))
                sistema.reservar_animal(id_animal, id_adotante)
            except ValueError:
                print("❌ Erro: Digite apenas números válidos.")

        elif opcao == "6":
            print(f"\n--- {G4}Realizar Adoção{RESET} ---")
            sistema.gerar_relatorio_animais()
            sistema.listar_adotantes()
            print("-" * 30)

            try:
                id_animal = int(input("Digite o ID do Animal: "))
                id_adotante = int(input("Digite o ID do Adotante: "))
                sistema.realizar_adocao(id_animal, id_adotante)
            except ValueError:
                print("❌ Erro: Digite apenas números válidos.")

        elif opcao == "7":
            print(f"\n--- {G3}Devolução{RESET} ---")
            sistema.gerar_relatorio_animais()
            print("-" * 30)
            
            try:
                id_animal = int(input("ID do Animal para devolver: "))
                
                print("\nQual o motivo da devolução?")
                print("1. Problema de Saúde (Doença)")
                print("2. Comportamento Agressivo (Mordeu/Atacou)")
                print("3. Outro motivo (Mudança, Alergia, etc)")
                escolha_motivo = input("Escolha: ")
                
                motivo_texto = ""
                if escolha_motivo == "1":
                    motivo_texto = "Problema de Saúde (Doença)"
                elif escolha_motivo == "2":
                    motivo_texto = "Comportamento Agressivo"
                elif escolha_motivo == "3":
                    motivo_texto = input("Digite o motivo detalhado: ")
                else:
                    print("Opção inválida. Registrando como motivo genérico.")
                    motivo_texto = "Motivo não especificado"

                sistema.processar_devolucao(id_animal, motivo_texto)
            except ValueError:
                print("❌ Erro: Digite apenas números válidos.")

        elif opcao == "8":
            sistema.gerar_relatorio_animais()
            try:
                id_animal = int(input("\nDigite o ID do Animal para editar: "))
                print(f"{G2}[Deixe vazio e aperte Enter para não alterar o valor atual]{RESET}")
                
                novo_nome = input("Novo Nome: ").strip() or None
                nova_raca = input("Nova Raça: ").strip() or None
                
                print("Novo Porte (1-P, 2-M, 3-G) [Enter para manter]:")
                escolha_porte = input("Escolha: ").strip()
                novo_porte = None
                if escolha_porte == "1": novo_porte = PorteAnimal.P
                elif escolha_porte == "2": novo_porte = PorteAnimal.M
                elif escolha_porte == "3": novo_porte = PorteAnimal.G

                novo_temp_str = input("Novo Temperamento (separe por vírgula): ").strip()
                novo_temperamento = [t.strip() for t in novo_temp_str.split(",")] if novo_temp_str else None

                dado_extra = None
                if 0 <= id_animal < len(sistema.animais):
                    animal_atual = sistema.animais[id_animal]
                    
                    if isinstance(animal_atual, Cachorro):
                        print(f"🐶 Editando um Cachorro. Passeio atual: {animal_atual._precisa_passeio}")
                        p_str = input("Precisa de muito passeio? (s/n) [Enter para manter]: ").strip().lower()
                        if p_str == 's':
                            dado_extra = True
                        elif p_str == 'n':
                            dado_extra = False
                            
                    elif isinstance(animal_atual, Gato):
                        print(f"🐱 Editando um Gato. Independência atual: {animal_atual._independencia}")
                        i_str = input("Nível de independência (0 a 5) [Enter para manter]: ").strip()
                        if i_str.isdigit():
                            dado_extra = int(i_str)

                sistema.editar_animal(id_animal, novo_nome, nova_raca, novo_porte, novo_temperamento, dado_extra)
            except ValueError:
                print("❌ Erro: Valor inválido inserido.")

        elif opcao == "9":
            sistema.gerar_relatorio_animais()
            try:
                id_animal = int(input("\nDigite o ID do Animal para EXCLUIR: "))
                confirmacao = input("Tem certeza absoluta? (s/n): ").lower()
                if confirmacao == 's':
                    sistema.excluir_animal(id_animal)
            except ValueError:
                print("❌ Erro: Digite apenas números.")

        elif opcao == "10":
            sistema.listar_adotantes()
            try:
                id_adotante = int(input("\nDigite o ID do Adotante para editar: "))
                print(f"{G2}[Deixe vazio e aperte Enter para não alterar]{RESET}")

                novo_nome = input("Novo Nome: ").strip() or None
                novo_contato = input("Novo Contato: ").strip() or None
                
                print("Nova Moradia (1-Casa, 2-Apto):")
                escolha_moradia = input("Escolha: ").strip()
                nova_moradia = None
                if escolha_moradia == "1": nova_moradia = TipoMoradia.CASA
                elif escolha_moradia == "2": nova_moradia = TipoMoradia.APTO

                nova_area_str = input("Nova Área útil: ").strip()
                nova_area = float(nova_area_str) if nova_area_str else None

                criancas_str = input("Tem crianças? (s/n): ").strip().lower()
                novas_criancas = None
                if criancas_str == 's': novas_criancas = True
                elif criancas_str == 'n': novas_criancas = False

                sistema.editar_adotante(id_adotante, novo_nome, novo_contato, nova_moradia, nova_area, novas_criancas)
            except ValueError:
                print("❌ Erro: Valor inválido.")

        elif opcao == "11":
            sistema.listar_adotantes()
            try:
                id_adotante = int(input("\nDigite o ID do Adotante para EXCLUIR: "))
                confirmacao = input("Tem certeza absoluta? (s/n): ").lower()
                if confirmacao == 's':
                    sistema.excluir_adotante(id_adotante)
            except ValueError:
                print("❌ Erro: Digite apenas números.")

        elif opcao == "12":
            sistema.gerar_relatorio_animais()
            try:
                id_animal = int(input("\nDigite o ID do animal para ver detalhes da fila: "))
                sistema.visualizar_detalhes_fila(id_animal)
            except ValueError:
                print("❌ Erro: Digite apenas números.")

        elif opcao == "13":
            sistema.processar_reservas_vencidas()

        elif opcao == "14":
            sistema.gerar_relatorios_estatisticos()

        elif opcao == "0":
            print(f"\n{G4}Saindo... Seus dados estão salvos! 💾{RESET}")
            break
        
        else:
            print("⚠️ Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
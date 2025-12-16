import sys
import os

sys.path.append(os.getcwd())

try:
    from src.adocao.services import SistemaAdocao
    from src.adocao.enums import PorteAnimal, TipoMoradia, StatusAnimal
    from src.adocao.domain import Cachorro, Gato
    from src.adocao.exceptions import AdocaoError
except ImportError as e:
    print("\n❌ Erro de Importação!")
    print("Certifique-se de executar este arquivo a partir da raiz do projeto.")
    print(f"Detalhe: {e}")
    sys.exit(1)

def escolher_temperamento_numerico():
    print("Temperamento:")
    print("1. Calmo/Dócil")
    print("2. Arisco/Agressivo")
    print("3. Outro (Digitar)")
    escolha = input("Escolha: ")
    
    if escolha == "1":
        return ["calmo"]
    elif escolha == "2":
        return ["arisco"]
    else:
        temp_str = input("Digite o temperamento (ex: brincalhão): ")
        return [t.strip() for t in temp_str.split(",")]
    
def menu_configuracoes(sistema):
    while True:
        print("\n⚙️  --- EDITOR DE CONFIGURAÇÕES (settings.json) ---")
        configs = sistema.settings
        
        chaves_editaveis = [k for k, v in configs.items() if not isinstance(v, dict)]
        
        for i, chave in enumerate(chaves_editaveis):
            valor = configs[chave]
            print(f"{i+1}. {chave.ljust(20)} : {valor}")
        
        print("0. Voltar")
        
        escolha = input("\nQual item deseja alterar? (Digite o número): ")
        
        if escolha == '0':
            break
            
        try:
            idx = int(escolha) - 1
            if 0 <= idx < len(chaves_editaveis):
                chave_selecionada = chaves_editaveis[idx]
                valor_atual = configs[chave_selecionada]
                
                print(f"\nAlterando: {chave_selecionada}")
                print(f"Valor atual: {valor_atual} (Tipo: {type(valor_atual).__name__})")
                
                if chave_selecionada == "banco_tipo":
                    print("Opções disponíveis:")
                    print("1. JSON")
                    print("2. SQLITE")
                    sel = input("👉 Escolha (1 ou 2): ").strip()
                    
                    if sel == "1":
                        novo_valor = "JSON"
                    elif sel == "2":
                        novo_valor = "SQLITE"
                    else:
                        print("❌ Opção inválida. Operação cancelada.")
                        continue 
                else:
                    novo_valor = input(f"👉 Digite o novo valor para '{chave_selecionada}': ")
                
                sucesso, msg = sistema.atualizar_configuracao(chave_selecionada, novo_valor)
                print(msg)
                
                if sucesso and chave_selecionada == "banco_tipo":
                    print("⚠️  AVISO: A alteração de Banco de Dados requer reinicialização do sistema.")
            else:
                print("❌ Número inválido.")
        except ValueError:
            print("❌ Digite um número válido.")
            
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
        print(f"\n=== 🐾 {G1}MENU PRINCIPAL{RESET} (Banco: {sistema.settings.get('banco_tipo', 'JSON')}) ===")
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
        print("15. ⚙️  Configurações") 
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
            
            temperamento = escolher_temperamento_numerico()

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

            temperamento = escolher_temperamento_numerico()

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
                sistema.buscar_animal(id_animal) # Lança erro se não existir

                id_adotante = int(input("Digite o ID do Adotante: "))
                sistema.buscar_adotante(id_adotante) # Lança erro se não existir

                sistema.reservar_animal(id_animal, id_adotante)
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "6":
            print(f"\n--- {G4}Realizar Adoção{RESET} ---")
            sistema.gerar_relatorio_animais()
            sistema.listar_adotantes()
            print("-" * 30)

            try:
                id_animal = int(input("Digite o ID do Animal: "))
                sistema.buscar_animal(id_animal) 

                id_adotante = int(input("Digite o ID do Adotante: "))
                sistema.buscar_adotante(id_adotante) 

                sistema.realizar_adocao(id_animal, id_adotante)
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "7":
            print(f"\n--- {G3}Devolução{RESET} ---")
            sistema.gerar_relatorio_animais(apenas_adotados=True)
            print("-" * 30)
            
            try:
                id_animal = int(input("ID do Animal para devolver: "))
                animal = sistema.buscar_animal(id_animal)
                if animal.status != StatusAnimal.ADOTADO:
                    print("❌ Erro: Este animal não está marcado como ADOTADO.")
                else:
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
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "8":
            sistema.gerar_relatorio_animais()
            try:
                id_animal = int(input("\nDigite o ID do Animal para editar: "))
                animal_atual = sistema.buscar_animal(id_animal) 
                
                print(f"{G2}[Deixe vazio e aperte Enter para não alterar o valor atual]{RESET}")
                
                novo_nome = input(f"Novo Nome [{animal_atual.nome}]: ").strip() or None
                nova_raca = input(f"Nova Raça [{animal_atual._raca}]: ").strip() or None
                
                print(f"Novo Porte (Atual: {animal_atual.porte.value})")
                print("1-P, 2-M, 3-G [Enter para manter]:")
                escolha_porte = input("Escolha: ").strip()
                novo_porte = None
                if escolha_porte == "1": novo_porte = PorteAnimal.P
                elif escolha_porte == "2": novo_porte = PorteAnimal.M
                elif escolha_porte == "3": novo_porte = PorteAnimal.G

                print(f"Temperamento Atual: {animal_atual.temperamento}")
                print("Deseja alterar o temperamento? (s/n)")
                mudar_temp = input("Escolha: ").lower()
                
                novo_temperamento = None
                if mudar_temp == 's':
                    novo_temperamento = escolher_temperamento_numerico()

                dado_extra = None
                
                if isinstance(animal_atual, Cachorro):

                    txt_passeio = "Sim" if animal_atual._precisa_passeio else "Não"
                    print(f"🐶 Editando um Cachorro. Passeio atual: {txt_passeio}")
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
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "9":
            sistema.gerar_relatorio_animais()
            try:

                id_animal = int(input("\nDigite o ID do Animal para EXCLUIR: "))
                sistema.buscar_animal(id_animal) 

                confirmacao = input("Tem certeza absoluta? (s/n): ").lower()
                if confirmacao == 's':
                    sistema.excluir_animal(id_animal)
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "10":
            sistema.listar_adotantes()
            try:

                id_adotante = int(input("\nDigite o ID do Adotante para editar: "))
                adotante_atual = sistema.buscar_adotante(id_adotante)

                print(f"{G2}[Deixe vazio e aperte Enter para não alterar]{RESET}")
                print(f"Editando: {adotante_atual.nome}")

                novo_nome = input(f"Novo Nome [{adotante_atual.nome}]: ").strip() or None
                novo_contato = input(f"Novo Contato [{adotante_atual.contato}]: ").strip() or None
                
                print(f"Nova Moradia (Atual: {adotante_atual.moradia.value})")
                print("1-Casa, 2-Apto [Enter para manter]:")
                escolha_moradia = input("Escolha: ").strip()
                nova_moradia = None
                if escolha_moradia == "1": nova_moradia = TipoMoradia.CASA
                elif escolha_moradia == "2": nova_moradia = TipoMoradia.APTO

                nova_area_str = input(f"Nova Área útil [{adotante_atual.area_util}]: ").strip()
                nova_area = float(nova_area_str) if nova_area_str else None

                txt_kids = "Sim" if adotante_atual.tem_criancas else "Não"
                print(f"Tem crianças? (Atual: {txt_kids})")
                criancas_str = input("Mudar? (s/n) [Enter para manter]: ").strip().lower()
                novas_criancas = None
                if criancas_str == 's': novas_criancas = True
                elif criancas_str == 'n': novas_criancas = False

                sistema.editar_adotante(id_adotante, novo_nome, novo_contato, nova_moradia, nova_area, novas_criancas)
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "11":
            sistema.listar_adotantes()
            try:
 
                id_adotante = int(input("\nDigite o ID do Adotante para EXCLUIR: "))
                sistema.buscar_adotante(id_adotante)

                confirmacao = input("Tem certeza absoluta? (s/n): ").lower()
                if confirmacao == 's':
                    sistema.excluir_adotante(id_adotante)
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "12":
            sistema.gerar_relatorio_animais()
            try:
                id_animal = int(input("\nDigite o ID do animal para ver detalhes da fila: "))
                sistema.visualizar_detalhes_fila(id_animal)
            except (ValueError, AdocaoError) as e:
                print(f"❌ Erro: {e}")

        elif opcao == "13":
            sistema.processar_reservas_vencidas()

        elif opcao == "14":
            sistema.gerar_relatorios_estatisticos()

        elif opcao == "15":
            menu_configuracoes(sistema)

        elif opcao == "0":
            print(f"\n{G4}Saindo... Seus dados estão salvos! 💾{RESET}")
            break
        
        else:
            print("⚠️ Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
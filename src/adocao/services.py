from typing import List
from .domain import Animal, Adotante, Cachorro, Gato
from .enums import StatusAnimal, PorteAnimal, TipoMoradia
from .repositories import Repositorio

class SistemaAdocao:
    def __init__(self):
        self.repo = Repositorio()
        # Carrega dados do disco assim que o sistema inicia
        self.animais: List[Animal] = self.repo.carregar_animais()
        self.adotantes: List[Adotante] = self.repo.carregar_adotantes()

    def cadastrar_cachorro(self, nome, raca, porte, precisa_passeio):
        # Cria o objeto Cachorro
        novo_pet = Cachorro(nome, raca, StatusAnimal.DISPONIVEL, porte, precisa_passeio)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais) # Salva no JSON
        print(f"✅ Cachorro {nome} cadastrado com sucesso!")

    def cadastrar_gato(self, nome, raca, porte, independencia):
        # Cria o objeto Gato
        novo_pet = Gato(nome, raca, StatusAnimal.DISPONIVEL, porte, independencia)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Gato {nome} cadastrado com sucesso!")

    def cadastrar_adotante(self, nome, contato, moradia, tem_criancas):
        novo_adotante = Adotante(nome, contato, moradia, tem_criancas)
        self.adotantes.append(novo_adotante)
        self.repo.salvar_adotantes(self.adotantes)
        print(f"👤 Adotante {nome} cadastrado!")

    def realizar_adocao_simples(self, indice_animal, indice_adotante):
        """
        Simula a relação entre Adotante e Animal mudando o status.
        (Futuramente teremos uma classe Adocao para isso).
        """
        try:
            animal = self.animais[indice_animal]
            adotante = self.adotantes[indice_adotante]
            
            if animal.status != StatusAnimal.DISPONIVEL:
                print(f"❌ O animal {animal.nome} não está disponível (Status: {animal.status.value}).")
                return

            # Regra de negócio simples: Mudar status para ADOTADO
            animal.mudar_status(StatusAnimal.ADOTADO)
            self.repo.salvar_animais(self.animais)
            print(f"🎉 Sucesso! {adotante.nome} adotou {animal.nome}!")
            
        except IndexError:
            print("❌ Erro: Índice de animal ou adotante inválido.")
        except Exception as e:
            print(f"❌ Erro ao realizar adoção: {e}")

    def gerar_relatorio_animais(self):
        print("\n--- 📊 RELATÓRIO DE ANIMAIS DO ABRIGO ---")
        print(f"Total de registros: {len(self.animais)}")
        
        # Filtros usando List Comprehension
        disponiveis = [a for a in self.animais if a.status == StatusAnimal.DISPONIVEL]
        adotados = [a for a in self.animais if a.status == StatusAnimal.ADOTADO]

        print(f"\n🟢 DISPONÍVEIS ({len(disponiveis)}):")
        if not disponiveis:
            print("   (Nenhum animal disponível no momento)")
        for a in disponiveis:
            print(f"   - {a}") # O Python usa o método __str__ do animal automaticamente
            
        print(f"\n🔴 JÁ ADOTADOS ({len(adotados)}):")
        if not adotados:
            print("   (Nenhum animal adotado ainda)")
        for a in adotados:
            print(f"   - {a}")
        print("-------------------------------------------")
    
    def listar_indices(self):
        """Ajuda o usuário a escolher os IDs para adoção"""
        print("\n🔢 Lista para Seleção:")
        print("--- ANIMAIS ---")
        for i, a in enumerate(self.animais):
            print(f"[{i}] {a.nome} ({a.status.value})")
            
        print("\n--- ADOTANTES ---")
        for i, a in enumerate(self.adotantes):
            print(f"[{i}] {a.nome}")
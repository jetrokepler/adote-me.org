from typing import List, Tuple, Optional
from .domain import Animal, Adotante, Cachorro, Gato
from .enums import StatusAnimal, PorteAnimal, TipoMoradia
from .repositories import Repositorio
from .strategies import FabricaTaxas 

class SistemaAdocao:
    def __init__(self):
        self.repo = Repositorio()
        self.animais: List[Animal] = self.repo.carregar_animais()
        self.adotantes: List[Adotante] = self.repo.carregar_adotantes()
        self.IDADE_MINIMA = 18
        self.AREA_MINIMA_PORTE_G = 40.0

    def cadastrar_cachorro(self, nome: str, raca: str, porte: PorteAnimal, temperamento: List[str], precisa_passeio: bool):
        novo_pet = Cachorro(nome, raca, StatusAnimal.DISPONIVEL, porte, temperamento, precisa_passeio)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Cachorro {nome} cadastrado!")

    def cadastrar_gato(self, nome: str, raca: str, porte: PorteAnimal, temperamento: List[str], independencia: int):
        novo_pet = Gato(nome, raca, StatusAnimal.DISPONIVEL, porte, temperamento, independencia)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Gato {nome} cadastrado!")

    def cadastrar_adotante(self, nome: str, contato: str, idade: int, moradia: TipoMoradia, area_util: float, tem_criancas: bool):
        novo_adotante = Adotante(nome, contato, idade, moradia, area_util, tem_criancas)
        self.adotantes.append(novo_adotante)
        self.repo.salvar_adotantes(self.adotantes)
        print(f"👤 Adotante {nome} cadastrado!")

    def _buscar_por_indice(self, idx_animal: int, idx_adotante: Optional[int] = None) -> Tuple[Animal, Optional[Adotante]]:
        try:
            animal = self.animais[idx_animal]
            adotante = self.adotantes[idx_adotante] if idx_adotante is not None else None
            return animal, adotante
        except IndexError:
            raise ValueError("Índice inválido.")

    def _validar_politica_adocao(self, animal: Animal, adotante: Adotante) -> Tuple[bool, str]:
        if adotante.idade < self.IDADE_MINIMA:
            return False, f"Adotante deve ter >= {self.IDADE_MINIMA} anos."

        if animal.porte == PorteAnimal.G:
            if adotante.moradia != TipoMoradia.CASA:
                return False, "Animais de Porte Grande exigem moradia em CASA."
            if adotante.area_util < self.AREA_MINIMA_PORTE_G:
                return False, f"Porte G exige área mínima de {self.AREA_MINIMA_PORTE_G}m²."

        if adotante.tem_criancas:
            temperamentos_pet = [t.lower() for t in animal.temperamento]
            if "arisco" in temperamentos_pet or "agressivo" in temperamentos_pet:
                return False, "Não permitido adotar animais 'ariscos' em casas com crianças."

        return True, "Aprovado"

    def reservar_animal(self, idx_animal: int, idx_adotante: int):
        try:
            animal, adotante = self._buscar_por_indice(idx_animal, idx_adotante)
            
            if animal.status != StatusAnimal.DISPONIVEL:
                print(f"❌ {animal.nome} não está disponível (Status: {animal.status.value}).")
                return
            
            aprovado, motivo = self._validar_politica_adocao(animal, adotante)
            if not aprovado:
                print(f"❌ Reserva negada pela política: {motivo}")
                return

            animal.mudar_status(StatusAnimal.RESERVADO)
            self.repo.salvar_animais(self.animais)
            print(f"🗓️  Reserva confirmada: {animal.nome} reservado para {adotante.nome}.")
            
        except ValueError as e: print(f"❌ {e}")

    def realizar_adocao(self, idx_animal: int, idx_adotante: int):
        try:
            animal, adotante = self._buscar_por_indice(idx_animal, idx_adotante)

            if animal.status not in [StatusAnimal.DISPONIVEL, StatusAnimal.RESERVADO]:
                print(f"❌ Erro: Status inválido ({animal.status.value}).")
                return

            aprovado, motivo = self._validar_politica_adocao(animal, adotante)
            if not aprovado:
                print(f"❌ Adoção negada: {motivo}")
                return

            estrategia = FabricaTaxas.obter_estrategia(animal, adotante)
            valor_taxa = estrategia.calcular(animal, adotante)
            
            animal.mudar_status(StatusAnimal.ADOTADO)
            self.repo.salvar_animais(self.animais)
            
            print(f"\n🎉 ADOÇÃO SUCESSO! {adotante.nome} adotou {animal.nome}!")
            print("="*40)
            print("          RECIBO DE ADOÇÃO")
            print("="*40)
            print(f"Animal: {animal.nome} ({animal.porte.value})")
            print(f"Tutor:  {adotante.nome}")
            print(f"Taxa:   R$ {valor_taxa}")
            print("="*40 + "\n")

        except ValueError as e: print(f"❌ {e}")

    def processar_devolucao(self, idx_animal: int, motivo: str):
        try:
            animal, _ = self._buscar_por_indice(idx_animal)
            if animal.status != StatusAnimal.ADOTADO:
                print(f"❌ Erro: Apenas animais adotados podem ser devolvidos.")
                return

            print(f"📝 Motivo: '{motivo}'")
            animal.mudar_status(StatusAnimal.DEVOLVIDO)

            if "doente" in motivo.lower() or "saude" in motivo.lower():
                animal.mudar_status(StatusAnimal.QUARENTENA)
            elif "mordeu" in motivo.lower() or "agressivo" in motivo.lower():
                animal.mudar_status(StatusAnimal.INADOTAVEL)
            else:
                animal.mudar_status(StatusAnimal.DISPONIVEL)

            self.repo.salvar_animais(self.animais)
            print(f"🔙 Devolução concluída. Novo status: {animal.status.value}.")
            
        except ValueError as e: print(f"❌ {e}")


    def vacinar_animal(self, idx_animal: int, nome_vacina: str):
        try:
            animal, _ = self._buscar_por_indice(idx_animal)
            if hasattr(animal, 'vacinar'):
                animal.vacinar(nome_vacina)
                self.repo.salvar_animais(self.animais)
                print(f"💉 {animal.nome} foi vacinado contra {nome_vacina}!")
            else:
                print(f"⚠️ {animal.nome} não pode ser vacinado (classe não suporta).")
        except ValueError as e: print(f"❌ {e}")

    def treinar_animal(self, idx_animal: int):
        try:
            animal, _ = self._buscar_por_indice(idx_animal)
            if hasattr(animal, 'treinar'):
                animal.treinar()
                self.repo.salvar_animais(self.animais)
                print(f"🎓 {animal.nome} recebeu treinamento! Nível atualizado.")
            else:
                print(f"⚠️ {animal.nome} não pode ser treinado (classe não suporta).")
        except ValueError as e: print(f"❌ {e}")

    def gerar_relatorio_animais(self):
        print("\n--- STATUS DO ABRIGO ---")
        for i, a in enumerate(self.animais):
            icone = "🟢" if a.status == StatusAnimal.DISPONIVEL else "🔴" if a.status == StatusAnimal.ADOTADO else "🟡"
            print(f"[{i}] {icone} {a.nome} (Porte {a.porte.value}, {a.status.value})")

    def listar_adotantes(self):
        print("\n--- ADOTANTES ---")
        for i, a in enumerate(self.adotantes):
            print(f"[{i}] {a.nome} ({a.moradia.value}, {a.area_util}m²)")

    def excluir_animal(self, idx_animal: int):
        try:
            self._buscar_por_indice(idx_animal)
            
            removido = self.animais.pop(idx_animal)
            self.repo.salvar_animais(self.animais)
            print(f"🗑️ Animal '{removido.nome}' removido com sucesso!")
        except ValueError as e: print(f"❌ {e}")
        except IndexError: print("❌ Índice inválido.")

    def excluir_adotante(self, idx_adotante: int):
        try:
            if idx_adotante < 0 or idx_adotante >= len(self.adotantes):
                raise ValueError("Índice inválido.")
            
            removido = self.adotantes.pop(idx_adotante)
            self.repo.salvar_adotantes(self.adotantes)
            print(f"🗑️ Adotante '{removido.nome}' removido com sucesso!")
        except ValueError as e: print(f"❌ {e}")

    def editar_animal(self, idx_animal: int, novo_nome=None, nova_raca=None, novo_porte=None, novo_temperamento=None, extra_dado=None):
        try:
            animal, _ = self._buscar_por_indice(idx_animal)
            
            if novo_nome: animal._nome = novo_nome
            if nova_raca: animal._raca = nova_raca
            if novo_porte: animal._porte = novo_porte
            if novo_temperamento: animal._temperamento = novo_temperamento

            if isinstance(animal, Cachorro) and extra_dado is not None:
                animal._precisa_passeio = extra_dado
            elif isinstance(animal, Gato) and extra_dado is not None:
                animal._independencia = extra_dado

            animal.adicionar_evento("Dados cadastrais editados manualmente.")
            self.repo.salvar_animais(self.animais)
            print(f"✏️ Dados de {animal.nome} atualizados!")
            
        except ValueError as e: print(f"❌ {e}")

    def editar_adotante(self, idx_adotante: int, novo_nome=None, novo_contato=None, nova_moradia=None, nova_area=None):
        try:
            if idx_adotante < 0 or idx_adotante >= len(self.adotantes):
                raise ValueError("Índice inválido.")
            
            adotante = self.adotantes[idx_adotante]

            if novo_nome: adotante._nome = novo_nome
            if novo_contato: adotante._contato = novo_contato
            if nova_moradia: adotante._moradia = nova_moradia
            if nova_area: adotante._area_util = nova_area

            self.repo.salvar_adotantes(self.adotantes)
            print(f"✏️ Dados de {adotante.nome} atualizados!")

        except ValueError as e: print(f"❌ {e}")
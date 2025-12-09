import unittest
from adocao.services import SistemaAdocao
from adocao.domain import Cachorro, Adotante
from adocao.enums import StatusAnimal, PorteAnimal, TipoMoradia

class TestServices(unittest.TestCase):

    def setUp(self):
        self.sistema = SistemaAdocao()
        # Mockando DB em memória
        self.sistema.animais = []
        self.sistema.adotantes = []

        # Cenários Prontos
        self.pet_grande = Cachorro("Hulk", "Pitbull", StatusAnimal.DISPONIVEL, PorteAnimal.G, [], True)
        self.pet_arisco = Cachorro("Zangado", "Pinscher", StatusAnimal.DISPONIVEL, PorteAnimal.P, ["arisco"], False)
        
        self.joao_apto = Adotante("Joao", "1", 30, TipoMoradia.APTO, 50.0, False)
        self.maria_casa = Adotante("Maria", "2", 30, TipoMoradia.CASA, 100.0, False)
        self.pedro_crianca = Adotante("Pedro", "3", 30, TipoMoradia.CASA, 100.0, True)
        self.enzo_menor = Adotante("Enzo", "4", 17, TipoMoradia.CASA, 100.0, False)

    # --- TESTES DE POLÍTICAS (Regras de Negócio) ---

    def test_regra_idade_minima(self):
        aprovado, motivo = self.sistema._validar_politica_adocao(self.pet_grande, self.enzo_menor)
        self.assertFalse(aprovado)
        self.assertIn("anos", motivo)

    def test_regra_porte_grande_apto(self):
        # Porte G não pode em Apartamento
        aprovado, _ = self.sistema._validar_politica_adocao(self.pet_grande, self.joao_apto)
        self.assertFalse(aprovado)

    def test_regra_porte_grande_casa_ok(self):
        # Porte G em Casa Grande -> OK
        aprovado, _ = self.sistema._validar_politica_adocao(self.pet_grande, self.maria_casa)
        self.assertTrue(aprovado)

    def test_regra_crianca_vs_arisco(self):
        # Criança + Arisco -> Bloqueia
        aprovado, _ = self.sistema._validar_politica_adocao(self.pet_arisco, self.pedro_crianca)
        self.assertFalse(aprovado)

    # --- TESTES DE FLUXOS DE PROCESSO ---

    def test_fluxo_devolucao_doenca(self):
        # Configura pet como ADOTADO para poder devolver
        self.pet_grande._status = StatusAnimal.ADOTADO
        self.sistema.animais.append(self.pet_grande)
        
        # Devolve por doença
        self.sistema.processar_devolucao(0, "Está muito doente")
        
        # Deve ir para QUARENTENA
        self.assertEqual(self.sistema.animais[0].status, StatusAnimal.QUARENTENA)

    def test_fluxo_devolucao_comum(self):
        # Configura pet como ADOTADO
        self.pet_grande._status = StatusAnimal.ADOTADO
        self.sistema.animais.append(self.pet_grande)
        
        # Devolve por mudança
        self.sistema.processar_devolucao(0, "Vou mudar de país")
        
        # Deve voltar para DISPONIVEL
        self.assertEqual(self.sistema.animais[0].status, StatusAnimal.DISPONIVEL)   
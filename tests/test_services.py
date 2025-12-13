import unittest
from src.adocao.services import SistemaAdocao
from src.adocao.domain import Cachorro, Adotante
from src.adocao.enums import StatusAnimal, PorteAnimal, TipoMoradia

class TestServices(unittest.TestCase):

    def setUp(self):
        self.sistema = SistemaAdocao()
        self.sistema.animais = []
        self.sistema.adotantes = []
        self.pet_padrao = Cachorro("Rex", "Vira-lata", StatusAnimal.DISPONIVEL, PorteAnimal.M, ["dócil"], True)
        self.adotante_padrao = Adotante("Joao", "1", 30, TipoMoradia.CASA, 100.0, False)

    def test_editar_animal(self):
        """Testa se conseguimos mudar o nome e um atributo específico do animal"""
        self.sistema.animais.append(self.pet_padrao)
        
        self.sistema.editar_animal(0, novo_nome="Rex Junior", extra_dado=False)
        
        self.assertEqual(self.sistema.animais[0].nome, "Rex Junior")
        self.assertFalse(self.sistema.animais[0]._precisa_passeio)

    def test_excluir_animal(self):
        """Testa se o animal é removido da lista"""
        self.sistema.animais.append(self.pet_padrao)
        self.assertEqual(len(self.sistema.animais), 1)
        
        self.sistema.excluir_animal(0)
        self.assertEqual(len(self.sistema.animais), 0)

    def test_editar_adotante(self):
        """Testa alteração de dados do adotante"""
        self.sistema.adotantes.append(self.adotante_padrao)
        
        self.sistema.editar_adotante(0, nova_moradia=TipoMoradia.APTO, nova_area=40.0)
        
        self.assertEqual(self.sistema.adotantes[0].moradia, TipoMoradia.APTO)
        self.assertEqual(self.sistema.adotantes[0].area_util, 40.0)

    def test_excluir_adotante(self):
        """Testa remoção de adotante"""
        self.sistema.adotantes.append(self.adotante_padrao)
        self.sistema.excluir_adotante(0)
        self.assertEqual(len(self.sistema.adotantes), 0)


    def test_regra_idade_minima(self):
        menor = Adotante("Enzo", "1", 17, TipoMoradia.CASA, 100.0, False)
        aprovado, motivo = self.sistema._validar_politica_adocao(self.pet_padrao, menor)
        self.assertFalse(aprovado)

    def test_regra_porte_grande_apto(self):
        pet_g = Cachorro("Hulk", "Pitbull", StatusAnimal.DISPONIVEL, PorteAnimal.G, [], True)
        adotante_apto = Adotante("Ana", "2", 30, TipoMoradia.APTO, 50.0, False)
        aprovado, _ = self.sistema._validar_politica_adocao(pet_g, adotante_apto)
        self.assertFalse(aprovado)

    def test_fluxo_devolucao_doenca(self):
        self.pet_padrao._status = StatusAnimal.ADOTADO
        self.sistema.animais.append(self.pet_padrao)
        self.sistema.processar_devolucao(0, "Está muito doente")
        self.assertEqual(self.sistema.animais[0].status, StatusAnimal.QUARENTENA)

if __name__ == '__main__':
    unittest.main()
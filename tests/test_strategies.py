import unittest
from src.adocao.strategies import FabricaTaxas, TaxaPadrao, TaxaSenior, TaxaPorteGrande
from src.adocao.domain import Cachorro, Adotante
from src.adocao.enums import StatusAnimal, PorteAnimal, TipoMoradia

class TestStrategies(unittest.TestCase):
    def setUp(self):
        # Mocks simples
        self.dog_pequeno = Cachorro("P", "R", StatusAnimal.DISPONIVEL, PorteAnimal.P, [], False)
        self.dog_grande = Cachorro("G", "R", StatusAnimal.DISPONIVEL, PorteAnimal.G, [], False)
        
        self.adotante_jovem = Adotante("J", "C", 25, TipoMoradia.CASA, 100.0, False)
        self.adotante_idoso = Adotante("S", "C", 65, TipoMoradia.CASA, 100.0, False)

    def test_taxa_padrao(self):
        # Jovem adotando animal pequeno -> Padrão (50.00)
        estrategia = FabricaTaxas.obter_estrategia(self.dog_pequeno, self.adotante_jovem)
        self.assertIsInstance(estrategia, TaxaPadrao)
        self.assertEqual(estrategia.calcular(self.dog_pequeno, self.adotante_jovem), 50.00)

    def test_taxa_senior(self):
        # Idoso adotando qualquer animal -> Desconto (20.00)
        estrategia = FabricaTaxas.obter_estrategia(self.dog_pequeno, self.adotante_idoso)
        self.assertIsInstance(estrategia, TaxaSenior)
        self.assertEqual(estrategia.calcular(self.dog_pequeno, self.adotante_idoso), 20.00)

    def test_taxa_porte_grande(self):
        # Jovem adotando animal grande -> Taxa maior (80.00)
        estrategia = FabricaTaxas.obter_estrategia(self.dog_grande, self.adotante_jovem)
        self.assertIsInstance(estrategia, TaxaPorteGrande)
        self.assertEqual(estrategia.calcular(self.dog_grande, self.adotante_jovem), 80.00)

if __name__ == '__main__':
    unittest.main() 
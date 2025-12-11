from abc import ABC, abstractmethod
from .domain import Animal, Adotante
from .enums import PorteAnimal

class EstrategiaTaxa(ABC):
    """Interface (Strategy) para cálculo de taxa de adoção."""
    
    @abstractmethod
    def calcular(self, animal: Animal, adotante: Adotante) -> float:
        pass

class TaxaPadrao(EstrategiaTaxa):
    """Cobrança padrão do abrigo."""
    def calcular(self, animal: Animal, adotante: Adotante) -> float:
        self.taxa = "50.00 (padrão)"
        return self.taxa

class TaxaSenior(EstrategiaTaxa):
    """
    Desconto para adotantes idosos (>60 anos) para incentivar
    a companhia na terceira idade.
    """
    def calcular(self, animal: Animal, adotante: Adotante) -> float:
        if adotante.idade >= 60:
            self.taxa = "20.00 (sênior)"
            return self.taxa 

class TaxaPorteGrande(EstrategiaTaxa):
    """
    Animais de porte grande têm custos maiores, logo a taxa é maior.
    """
    def calcular(self, animal: Animal, adotante: Adotante) -> float:
        if animal.porte == PorteAnimal.G:
            self.taxa = "80.00 (porte grande)"
            return self.taxa


class FabricaTaxas:
    """
    Factory simples para decidir qual estratégia usar automaticamente.
    """
    @staticmethod
    def obter_estrategia(animal: Animal, adotante: Adotante) -> EstrategiaTaxa:
        # Prioridade 1: Se adotante for idoso, aplica desconto Sénior
        if adotante.idade >= 60:
            return TaxaSenior()
        
        # Prioridade 2: Se animal for Grande, aplica taxa maior
        if animal.porte == PorteAnimal.G:
            return TaxaPorteGrande()
            
        # Padrão
        return TaxaPadrao()
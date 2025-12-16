from abc import ABC, abstractmethod
from .domain import Animal, Adotante
from .enums import PorteAnimal

class EstrategiaTaxa(ABC):
    """Interface (Strategy) para cálculo de taxa de adoção."""
    
    @abstractmethod
    def calcular(self, animal: Animal, adotante: Adotante) -> str:
        """Calcula a taxa de adoção baseada na estratégia definida.

        Args:
            animal (Animal): O animal a ser adotado.
            adotante (Adotante): O potencial adotante.

        Returns:
            str: O valor da taxa calculado.
        """
        pass

class TaxaPadrao(EstrategiaTaxa):
    """Implementa a cobrança padrão do abrigo."""

    def calcular(self, animal: Animal, adotante: Adotante) -> str:
        """Aplica a taxa padrão para adoções.

        Args:
            animal (Animal): O animal a ser adotado.
            adotante (Adotante): O adotante.

        Returns:
            str: O valor da taxa padrão formatado.
        """
        self.taxa = "50.00 (padrão)"
        return self.taxa

class TaxaSenior(EstrategiaTaxa):
    """Implementa desconto para adotantes idosos para incentivar a companhia na terceira idade."""

    def calcular(self, animal: Animal, adotante: Adotante) -> str:
        """Calcula a taxa com desconto se o adotante for idoso.

        Args:
            animal (Animal): O animal a ser adotado.
            adotante (Adotante): O adotante.

        Returns:
            str: O valor da taxa com desconto sênior.
        """
        if adotante.idade >= 60:
            self.taxa = "20.00 (sênior)"
            return self.taxa 

class TaxaPorteGrande(EstrategiaTaxa):
    """Implementa taxa diferenciada para animais de porte grande devido aos custos maiores."""

    def calcular(self, animal: Animal, adotante: Adotante) -> str:
        """Calcula a taxa majorada se o animal for de grande porte.

        Args:
            animal (Animal): O animal a ser adotado.
            adotante (Adotante): O adotante.

        Returns:
            str: O valor da taxa para porte grande.
        """
        if animal.porte == PorteAnimal.G:
            self.taxa = "80.00 (porte grande)"
            return self.taxa

class FabricaTaxas:
    """Factory para decidir qual estratégia de taxa usar automaticamente."""

    @staticmethod
    def obter_estrategia(animal: Animal, adotante: Adotante) -> EstrategiaTaxa:
        """Determina a estratégia de taxa adequada baseada nas regras de prioridade.

        Args:
            animal (Animal): O animal a ser adotado.
            adotante (Adotante): O adotante.

        Returns:
            EstrategiaTaxa: A instância da estratégia de taxa selecionada.
        """
        if adotante.idade >= 60:
            return TaxaSenior()
        
        if animal.porte == PorteAnimal.G:
            return TaxaPorteGrande()
            
        return TaxaPadrao()
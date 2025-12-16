import unittest
import time
from unittest.mock import patch
from src.adocao.domain import FilaEspera, Adotante, Cachorro
from src.adocao.services import SistemaAdocao
from src.adocao.enums import TipoMoradia, StatusAnimal, PorteAnimal

class TestFilaPrioridade(unittest.TestCase):

    def setUp(self):
        # Configuração básica para testes de ordenação pura
        self.fila = FilaEspera()
        
        # Mocks de Adotantes para teste de ordenação
        self.adotante_top = Adotante("Top", "1", 40, TipoMoradia.CASA, 100.0, False)
        self.adotante_medio = Adotante("Medio", "2", 25, TipoMoradia.CASA, 50.0, False)
        self.adotante_baixo = Adotante("Baixo", "3", 18, TipoMoradia.APTO, 30.0, True)

        # --- SETUP PARA TESTES DE REGRAS DE SISTEMA ---
        self.sistema = SistemaAdocao()
        self.sistema.animais = []
        self.sistema.adotantes = []

        # Animal Grande (Exige Casa)
        self.dog_grande = Cachorro("Hulk", "Dogue", StatusAnimal.DISPONIVEL, PorteAnimal.G, [], True)
        
        # Adotantes para os cenários complexos
        self.pessoa_apto = Adotante("Enzo", "111", 25, TipoMoradia.APTO, 60.0, False) # Inelegível p/ G
        self.pessoa_casa_a = Adotante("Ana", "222", 30, TipoMoradia.CASA, 100.0, False)
        self.pessoa_casa_b = Adotante("Beto", "333", 30, TipoMoradia.CASA, 100.0, False)

    # --- TESTES UNITÁRIOS DA FILA (ORDENAÇÃO) ---

    def test_ordenacao_score(self):
        """Testa se maior score fica em primeiro."""
        self.fila.adicionar(self.adotante_baixo, score=20)
        self.fila.adicionar(self.adotante_top, score=90)
        self.fila.adicionar(self.adotante_medio, score=50)

        # O primeiro a sair deve ser o de score 90
        primeiro = self.fila.proximo()
        self.assertEqual(primeiro.nome, "Top")
        
        segundo = self.fila.proximo()
        self.assertEqual(segundo.nome, "Medio")

    def test_criterio_desempate_tempo(self):
        """Testa se scores iguais respeitam a ordem de chegada."""
        self.fila.adicionar(self.adotante_medio, score=50)
        time.sleep(0.01) # Garante timestamp diferente
        self.fila.adicionar(self.adotante_top, score=50)

        primeiro = self.fila.proximo()
        self.assertEqual(primeiro.nome, "Medio") # Chegou antes

    # --- TESTES DE REGRAS DE NEGÓCIO ---

    def test_bloqueio_inelegivel_na_fila(self):
        """
        Cenário: Fila de animal exige CASA. Pessoa de APTO tenta.
        Resultado: Bloqueio imediato pela política.
        """
        self.sistema.animais.append(self.dog_grande)
        self.sistema.adotantes.append(self.pessoa_apto) 

        # Tenta Reservar - Política deve barrar antes de qualquer coisa
        aprovado, motivo = self.sistema._validar_politica_adocao(self.dog_grande, self.pessoa_apto)
        
        self.assertFalse(aprovado)
        # CORREÇÃO AQUI: Ajustado para "exigem" (plural) conforme services.py
        self.assertIn("exigem moradia em CASA", motivo)

    def test_bloqueio_fura_fila_adocao(self):
        """
        Cenário: Animal reservado para Ana. Beto tenta adotar.
        Resultado: Bloqueio.
        """
        self.sistema.animais.append(self.dog_grande)
        self.sistema.adotantes.append(self.pessoa_casa_a) # Ana (ID 0)
        self.sistema.adotantes.append(self.pessoa_casa_b) # Beto (ID 1)

        # Ana Reserva
        self.sistema.reservar_animal(0, 0)
        
        # Beto tenta Adotar
        self.sistema.realizar_adocao(0, 1)

        # Verificação: Status NÃO mudou para ADOTADO (continuou RESERVADO)
        self.assertEqual(self.sistema.animais[0].status, StatusAnimal.RESERVADO)

    @patch('builtins.input', return_value='n') 
    def test_bloqueio_reserva_duplicada(self, mock_input):
        """
        Cenário: Ana já reservou. Ana tenta reservar de novo.
        O sistema vai perguntar "Quer entrar na fila?".
        O @patch vai responder 'n' automaticamente para o teste não travar.
        """
        self.sistema.animais.append(self.dog_grande)
        self.sistema.adotantes.append(self.pessoa_casa_a)

        # 1. Primeira Reserva
        self.sistema.reservar_animal(0, 0)
        data_original = self.sistema.animais[0].data_reserva
        time.sleep(0.1)

        # 2. Segunda Tentativa (Mesma pessoa)
        # Graças ao @patch, o input será ignorado (respondido com 'n')
        self.sistema.reservar_animal(0, 0)

        # Verificação: A data da reserva NÃO deve ter sido atualizada (não renova prazo)
        self.assertEqual(self.sistema.animais[0].data_reserva, data_original)
        self.assertEqual(self.sistema.animais[0].nome_reservante, "Ana")

if __name__ == '__main__':
    unittest.main()
import unittest
from datetime import date
from adocao.domain import Cachorro, Gato, Adotante
from adocao.enums import StatusAnimal, PorteAnimal, TipoMoradia

class TestDomain(unittest.TestCase):

    def setUp(self):
        self.dog = Cachorro("Rex", "Vira-lata", StatusAnimal.DISPONIVEL, PorteAnimal.M, [], True)
        self.cat = Gato("Mimi", "Persa", StatusAnimal.DISPONIVEL, PorteAnimal.P, [], 1)

    # --- TESTES DE SERIALIZAÇÃO (JSON) ---
    def test_adotante_to_dict(self):
        adotante = Adotante("Ana", "123", 25, TipoMoradia.CASA, 100.0, False)
        dados = adotante.to_dict()
        self.assertEqual(dados["nome"], "Ana")
        self.assertEqual(dados["idade"], 25)
        self.assertEqual(dados["area_util"], 100.0)

    # --- TESTES DE MÁQUINA DE ESTADOS (Status) ---
    def test_transicao_status_valida(self):
        # Disponível -> Reservado -> Adotado
        self.dog.mudar_status(StatusAnimal.RESERVADO)
        self.assertEqual(self.dog.status, StatusAnimal.RESERVADO)
        self.dog.mudar_status(StatusAnimal.ADOTADO)
        self.assertEqual(self.dog.status, StatusAnimal.ADOTADO)

    def test_transicao_status_invalida(self):
        # Disponível -> Devolvido (Não pode pular etapas)
        with self.assertRaises(ValueError):
            self.dog.mudar_status(StatusAnimal.DEVOLVIDO)

    # --- TESTES DOS MIXINS (Requisitos Técnicos) ---
    def test_mixin_vacinavel(self):
        self.dog.vacinar("Raiva")
        self.assertIn("Raiva", self.dog.agenda_vacinas)
        # Verifica se o evento foi pro histórico
        ultimo_evento = self.dog.historico_eventos[-1]
        self.assertIn("Vacinado contra Raiva", ultimo_evento)

    def test_mixin_adestravel(self):
        nivel_inicial = self.dog.nivel_adestramento
        self.dog.treinar()
        self.assertEqual(self.dog.nivel_adestramento, nivel_inicial + 1)
        # Gato não tem AdestravelMixin, então não testamos nele
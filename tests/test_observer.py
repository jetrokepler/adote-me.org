import os
import sys
import pytest
from unittest.mock import MagicMock

# Ajuste de caminho para encontrar o 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.adocao.services import SistemaAdocao, LoggerObserver
from src.adocao.domain import Cachorro, Adotante
from src.adocao.enums import PorteAnimal, TipoMoradia, StatusAnimal
from src.adocao.repositories import RepositorioSQLite

# --- TESTE 1: O Observer está a "fofocar" corretamente? ---
def test_observer_notificacao():
    sistema = SistemaAdocao()
    
    # Criamos um "espião" (Mock) para fingir que é um observador
    espião = MagicMock()
    sistema.adicionar_observador(espião)
    
    # Simulamos uma notificação manual
    mensagem = "Teste de Notificação QA"
    sistema.notificar_observadores(mensagem)
    
    # O teste passa se o método 'atualizar' foi chamado com a mensagem certa
    espião.atualizar.assert_called_with(mensagem)
    print("\n✅ [Observer] Sistema notificou corretamente!")

def test_observer_arquivo_log():
    # Teste real de escrita em arquivo
    arquivo_teste = "teste_log_qa.log"
    logger = LoggerObserver(arquivo_teste)
    
    mensagem = "Evento de Teste no Arquivo"
    logger.atualizar(mensagem)
    
    caminho = os.path.join("dados", arquivo_teste)
    assert os.path.exists(caminho)
    
    with open(caminho, 'r') as f:
        conteudo = f.read()
    
    assert mensagem in conteudo
    print("✅ [Observer] Arquivo de log criado e escrito com sucesso!")
    
    # Limpeza
    os.remove(caminho)

# --- TESTE 2: O SQLite aguenta Listas e Enums? ---
def test_sqlite_persistencia_complexa():
    # Força uso do SQLite para este teste
    repo = RepositorioSQLite()
    # Usa um banco de teste para não estragar o oficial
    repo.db_name = "test_qa.db" 
    repo._inicializar_banco()
    
    # Dado complexo: Enum (Porte) e Lista (Temperamento)
    cao = Cachorro("DogQA", "Robot", StatusAnimal.DISPONIVEL, PorteAnimal.G, ["bit", "byte"], True)
    
    # 1. Salvar
    repo.salvar_animais([cao])
    
    # 2. Carregar (Aqui é onde costuma dar erro se não tratar a string)
    animais_carregados = repo.carregar_animais()
    
    assert len(animais_carregados) == 1
    recuperado = animais_carregados[0]
    
    # Verificações Críticas
    assert recuperado.nome == "DogQA"
    assert recuperado.porte == PorteAnimal.G  # Verifica se voltou como Enum
    assert isinstance(recuperado.temperamento, list) # Verifica se voltou como Lista
    assert "bit" in recuperado.temperamento
    
    print("✅ [SQLite] Persistência de listas e Enums funcionou!")
    
    # Limpeza
    if os.path.exists("test_qa.db"):
        os.remove("test_qa.db")

if __name__ == "__main__":
    # Roda os testes manualmente se executar este arquivo
    try:
        test_observer_notificacao()
        test_observer_arquivo_log()
        test_sqlite_persistencia_complexa()
        print("\n🎉 TODOS OS TESTES PASSARAM! O SISTEMA ESTÁ ROBUSTO.")
    except AssertionError as e:
        print(f"\n❌ FALHA NO TESTE: {e}")
    except Exception as e:
        print(f"\n❌ ERRO TÉCNICO: {e}")
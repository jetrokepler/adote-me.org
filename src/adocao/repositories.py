import json
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import List
from .domain import Animal, Adotante

class Repositorio(ABC):
    """Classe abstrata que define a interface para persistência de dados."""

    @abstractmethod
    def salvar_animais(self, animais: List[Animal]) -> None:
        """Salva a lista de animais no meio de persistência.

        Args:
            animais (List[Animal]): Lista de instâncias de Animal a serem salvas.
        """
        pass

    @abstractmethod
    def carregar_animais(self) -> List[Animal]:
        """Carrega a lista de animais do meio de persistência.

        Returns:
            List[Animal]: Lista contendo os objetos Animal carregados.
        """
        pass

    @abstractmethod
    def salvar_adotantes(self, adotantes: List[Adotante]) -> None:
        """Salva a lista de adotantes no meio de persistência.

        Args:
            adotantes (List[Adotante]): Lista de instâncias de Adotante a serem salvas.
        """
        pass

    @abstractmethod
    def carregar_adotantes(self) -> List[Adotante]:
        """Carrega a lista de adotantes do meio de persistência.

        Returns:
            List[Adotante]: Lista contendo os objetos Adotante carregados.
        """
        pass

class RepositorioJSON(Repositorio):
    """Implementação do repositório utilizando arquivos JSON para armazenamento.

    Attributes:
        arquivo_animais (str): Caminho do arquivo JSON de animais.
        arquivo_adotantes (str): Caminho do arquivo JSON de adotantes.
    """

    def __init__(self) -> None:
        """Inicializa o repositório JSON definindo os nomes dos arquivos."""
        self.arquivo_animais = "animais.json"
        self.arquivo_adotantes = "adotantes.json"

    def salvar_animais(self, animais: List[Animal]) -> None:
        """Salva a lista de animais serializando para um arquivo JSON.

        Args:
            animais (List[Animal]): Lista de animais a serem persistidos.
        """
        dados = [animal.to_dict() for animal in animais]
        try:
            with open(self.arquivo_animais, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar animais (JSON): {e}")

    def carregar_animais(self) -> List[Animal]:
        """Lê o arquivo JSON e reconstrói a lista de objetos Animal.

        Returns:
            List[Animal]: Lista de animais carregados ou lista vazia em caso de erro/arquivo inexistente.
        """
        if not os.path.exists(self.arquivo_animais):
            return []
        try:
            with open(self.arquivo_animais, 'r', encoding='utf-8') as f:
                dados_brutos = json.load(f)
            
            lista_objetos = []
            for item in dados_brutos:
                obj = Animal.from_dict(item)
                if obj:
                    lista_objetos.append(obj)
            return lista_objetos
        except Exception as e:
            print(f"Erro ao carregar animais (JSON): {e}")
            return []

    def salvar_adotantes(self, adotantes: List[Adotante]) -> None:
        """Salva a lista de adotantes serializando para um arquivo JSON.

        Args:
            adotantes (List[Adotante]): Lista de adotantes a serem persistidos.
        """
        dados = [adotante.to_dict() for adotante in adotantes]
        try:
            with open(self.arquivo_adotantes, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar adotantes (JSON): {e}")

    def carregar_adotantes(self) -> List[Adotante]:
        """Lê o arquivo JSON e reconstrói a lista de objetos Adotante.

        Returns:
            List[Adotante]: Lista de adotantes carregados ou lista vazia em caso de erro/arquivo inexistente.
        """
        if not os.path.exists(self.arquivo_adotantes):
            return []
        try:
            with open(self.arquivo_adotantes, 'r', encoding='utf-8') as f:
                dados_brutos = json.load(f)
            return [Adotante.from_dict(item) for item in dados_brutos]
        except Exception as e:
            print(f"Erro ao carregar adotantes (JSON): {e}")
            return []

class RepositorioSQLite(Repositorio):
    """Implementação do repositório utilizando banco de dados SQLite.
    
    Os objetos são serializados em JSON e armazenados em colunas de texto no banco.

    Attributes:
        db_name (str): Nome do arquivo do banco de dados.
    """

    def __init__(self) -> None:
        """Inicializa o repositório SQLite e garante que as tabelas existam."""
        self.db_name = "adocao.db"
        self._inicializar_banco()

    def _get_conexao(self) -> sqlite3.Connection:
        """Cria e retorna uma conexão com o banco de dados.

        Returns:
            sqlite3.Connection: Objeto de conexão do SQLite.
        """
        return sqlite3.connect(self.db_name)

    def _inicializar_banco(self) -> None:
        """Cria as tabelas 'animais' e 'adotantes' caso não existam."""
        conn = self._get_conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS animais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dados_json TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adotantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dados_json TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()

    def salvar_animais(self, animais: List[Animal]) -> None:
        """Salva a lista de animais no banco de dados.
        
        Nota: A implementação atual limpa a tabela e reinsere os dados.

        Args:
            animais (List[Animal]): Lista de animais a serem salvos.
        """
        conn = self._get_conexao()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM animais")
            
            for animal in animais:
                dados_string = json.dumps(animal.to_dict(), ensure_ascii=False)
                cursor.execute("INSERT INTO animais (dados_json) VALUES (?)", (dados_string,))
            
            conn.commit()
        except Exception as e:
            print(f"Erro ao salvar animais (SQLite): {e}")
        finally:
            conn.close()

    def carregar_animais(self) -> List[Animal]:
        """Carrega todos os animais armazenados no banco de dados.

        Returns:
            List[Animal]: Lista de objetos Animal reconstruídos a partir do JSON armazenado.
        """
        conn = self._get_conexao()
        cursor = conn.cursor()
        lista_objetos = []
        
        try:
            cursor.execute("SELECT dados_json FROM animais")
            linhas = cursor.fetchall()
            
            for linha in linhas:
                dicionario = json.loads(linha[0])
                obj = Animal.from_dict(dicionario)
                if obj:
                    lista_objetos.append(obj)
                    
        except Exception as e:
            print(f"Erro ao carregar animais (SQLite): {e}")
        finally:
            conn.close()
            
        return lista_objetos

    def salvar_adotantes(self, adotantes: List[Adotante]) -> None:
        """Salva a lista de adotantes no banco de dados.

        Nota: A implementação atual limpa a tabela e reinsere os dados.

        Args:
            adotantes (List[Adotante]): Lista de adotantes a serem salvos.
        """
        conn = self._get_conexao()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM adotantes")
            
            for adotante in adotantes:
                dados_string = json.dumps(adotante.to_dict(), ensure_ascii=False)
                cursor.execute("INSERT INTO adotantes (dados_json) VALUES (?)", (dados_string,))
            
            conn.commit()
        except Exception as e:
            print(f"Erro ao salvar adotantes (SQLite): {e}")
        finally:
            conn.close()

    def carregar_adotantes(self) -> List[Adotante]:
        """Carrega todos os adotantes armazenados no banco de dados.

        Returns:
            List[Adotante]: Lista de objetos Adotante reconstruídos a partir do JSON armazenado.
        """
        conn = self._get_conexao()
        cursor = conn.cursor()
        lista_objetos = []
        
        try:
            cursor.execute("SELECT dados_json FROM adotantes")
            linhas = cursor.fetchall()
            
            for linha in linhas:
                dicionario = json.loads(linha[0])
                obj = Adotante.from_dict(dicionario)
                if obj:
                    lista_objetos.append(obj)
                    
        except Exception as e:
            print(f"Erro ao carregar adotantes (SQLite): {e}")
        finally:
            conn.close()
            
        return lista_objetos
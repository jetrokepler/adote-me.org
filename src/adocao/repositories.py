import json
import os
import sqlite3
from abc import ABC, abstractmethod
from typing import List
from .domain import Animal, Adotante

class Repositorio(ABC):
    @abstractmethod
    def salvar_animais(self, animais: List[Animal]):
        pass

    @abstractmethod
    def carregar_animais(self) -> List[Animal]:
        pass

    @abstractmethod
    def salvar_adotantes(self, adotantes: List[Adotante]):
        pass

    @abstractmethod
    def carregar_adotantes(self) -> List[Adotante]:
        pass

class RepositorioJSON(Repositorio):
    def __init__(self):
        self.arquivo_animais = "animais.json"
        self.arquivo_adotantes = "adotantes.json"

    def salvar_animais(self, animais: List[Animal]):
        dados = [animal.to_dict() for animal in animais]
        try:
            with open(self.arquivo_animais, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar animais (JSON): {e}")

    def carregar_animais(self) -> List[Animal]:
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

    def salvar_adotantes(self, adotantes: List[Adotante]):
        dados = [adotante.to_dict() for adotante in adotantes]
        try:
            with open(self.arquivo_adotantes, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar adotantes (JSON): {e}")

    def carregar_adotantes(self) -> List[Adotante]:
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
    def __init__(self):
        self.db_name = "adocao.db"
        self._inicializar_banco()

    def _get_conexao(self):
        return sqlite3.connect(self.db_name)

    def _inicializar_banco(self):
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

    def salvar_animais(self, animais: List[Animal]):
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

    def salvar_adotantes(self, adotantes: List[Adotante]):
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
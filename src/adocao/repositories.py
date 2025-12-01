import json
import os
from typing import List
from .domain import Animal, Adotante

class Repositorio:
    def __init__(self):
        self.arquivo_animais = "animais.json"
        self.arquivo_adotantes = "adotantes.json"

    def salvar_animais(self, animais: List[Animal]):
        # Transforma objetos em dicionários
        dados = [animal.to_dict() for animal in animais]
        try:
            with open(self.arquivo_animais, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            print("💾 Animais salvos com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar animais: {e}")

    def carregar_animais(self) -> List[Animal]:
        if not os.path.exists(self.arquivo_animais):
            return []
        
        try:
            with open(self.arquivo_animais, 'r', encoding='utf-8') as f:
                dados_brutos = json.load(f)
            
            # Transforma dicionários de volta em objetos (usando a Factory do Animal)
            lista_objetos = []
            for item in dados_brutos:
                obj = Animal.from_dict(item)
                if obj:
                    lista_objetos.append(obj)
            return lista_objetos
        except Exception as e:
            print(f"Erro ao carregar animais: {e}")
            return []

    def salvar_adotantes(self, adotantes: List[Adotante]):
        dados = [adotante.to_dict() for adotante in adotantes]
        try:
            with open(self.arquivo_adotantes, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            print("💾 Adotantes salvos com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar adotantes: {e}")

    def carregar_adotantes(self) -> List[Adotante]:
        if not os.path.exists(self.arquivo_adotantes):
            return []
        
        try:
            with open(self.arquivo_adotantes, 'r', encoding='utf-8') as f:
                dados_brutos = json.load(f)
            return [Adotante.from_dict(item) for item in dados_brutos]
        except Exception as e:
            print(f"Erro ao carregar adotantes: {e}")
            return []
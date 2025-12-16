import json
import os
from typing import List, Tuple, Optional
from datetime import datetime, timedelta
from .domain import Animal, Adotante, Cachorro, Gato
from .enums import StatusAnimal, PorteAnimal, TipoMoradia
from .repositories import RepositorioJSON, RepositorioSQLite
from .strategies import FabricaTaxas
from abc import ABC, abstractmethod
from .exceptions import (
    AdocaoError, 
    EntidadeNaoEncontradaError, 
    PoliticaNaoAtendidaError, 
    ReservaInvalidaError, 
    TransicaoStatusError
)

class Observador(ABC):
    @abstractmethod
    def atualizar(self, mensagem: str):
        pass

class LoggerObserver(Observador):
    def __init__(self, arquivo="historico_eventos.log"):
        self.arquivo = arquivo

    def atualizar(self, mensagem: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {mensagem}\n"
        try:
            pasta = "dados"
            if not os.path.exists(pasta):
                os.makedirs(pasta)
            caminho = os.path.join(pasta, self.arquivo)
            with open(caminho, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Erro ao gravar log: {e}")

class SistemaAdocao:
    def __init__(self):
        self.settings = self._carregar_settings()
        
        tipo_banco = self.settings.get("banco_tipo", "JSON").upper()
        
        if tipo_banco == "SQLITE":
            print("💾 Usando Banco de Dados SQLite")
            self.repo = RepositorioSQLite()
        else:
            print("💾 Usando Arquivos JSON")
            self.repo = RepositorioJSON()

        self.animais: List[Animal] = self.repo.carregar_animais()
        self.adotantes: List[Adotante] = self.repo.carregar_adotantes()

        self.observadores: List[Observador] = []
        self.adicionar_observador(LoggerObserver())

    def adicionar_observador(self, observador: Observador):
        self.observadores.append(observador)

    def notificar_observadores(self, evento: str):
        for obs in self.observadores:
            obs.atualizar(evento)

    def _carregar_settings(self):
        padrao = {
            "banco_tipo": "JSON",
            "idade_minima": 18,
            "reserva_horas": 48,
            "area_minima_g": 40.0,
            "pesos_compatibilidade": {
                "moradia": 40,
                "criancas": 30,
                "experiencia": 20,
                "idade_energia": 10
            }
        }
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding='utf-8') as f:
                    dados = json.load(f)
                    padrao.update(dados)
        except Exception as e:
            print(f"⚠️ Erro ao ler settings.json: {e}")
        
        if not os.path.exists("settings.json"):
            self._salvar_settings_arquivo(padrao)
            
        return padrao

    def _salvar_settings_arquivo(self, dados):
        try:
            with open("settings.json", "w", encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar settings: {e}")

    def atualizar_configuracao(self, chave, novo_valor):
        if chave in self.settings:
            tipo_original = type(self.settings[chave])
            
            try:
                if tipo_original == int:
                    valor_convertido = int(novo_valor)
                elif tipo_original == float:
                    valor_convertido = float(novo_valor)
                elif tipo_original == bool:
                    valor_convertido = str(novo_valor).lower() in ['true', '1', 's', 'sim']
                elif isinstance(self.settings[chave], dict):
                    return False, "❌ Não é possível editar dicionários complexos por este menu."
                else:
                    valor_convertido = str(novo_valor)
                
                self.settings[chave] = valor_convertido
                self._salvar_settings_arquivo(self.settings)
                return True, f"✅ '{chave}' atualizado para: {valor_convertido}"
            except ValueError:
                return False, f"❌ Erro: O valor deve ser do tipo {tipo_original.__name__}."
        else:
            return False, "❌ Chave de configuração não encontrada."

    def buscar_animal(self, idx: int) -> Animal:
        try:
            return self.animais[idx]
        except IndexError:
            raise EntidadeNaoEncontradaError(f"Animal com índice {idx} não encontrado.")

    def buscar_adotante(self, idx: int) -> Adotante:
        try:
            return self.adotantes[idx]
        except IndexError:
            raise EntidadeNaoEncontradaError(f"Adotante com índice {idx} não encontrado.")

    def cadastrar_cachorro(self, nome: str, raca: str, porte: PorteAnimal, temperamento: List[str], precisa_passeio: bool):
        novo_pet = Cachorro(nome, raca, StatusAnimal.DISPONIVEL, porte, temperamento, precisa_passeio)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Cachorro {nome} cadastrado com sucesso!")

    def cadastrar_gato(self, nome: str, raca: str, porte: PorteAnimal, temperamento: List[str], independencia: int):
        novo_pet = Gato(nome, raca, StatusAnimal.DISPONIVEL, porte, temperamento, independencia)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Gato {nome} cadastrado com sucesso!")

    def cadastrar_adotante(self, nome: str, contato: str, idade: int, moradia: TipoMoradia, area_util: float, tem_criancas: bool):
        novo_adotante = Adotante(nome, contato, idade, moradia, area_util, tem_criancas)
        self.adotantes.append(novo_adotante)
        self.repo.salvar_adotantes(self.adotantes)
        print(f"👤 Adotante {nome} cadastrado com sucesso!")

    def excluir_animal(self, idx_animal: int):
        try:
            self.buscar_animal(idx_animal)
            removido = self.animais.pop(idx_animal)
            self.repo.salvar_animais(self.animais)
            print(f"🗑️ Animal '{removido.nome}' removido com sucesso!")
        except (ValueError, AdocaoError) as e:
            print(f"❌ Índice inválido ou erro: {e}")

    def excluir_adotante(self, idx_adotante: int):
        try:
            self.buscar_adotante(idx_adotante)
            removido = self.adotantes.pop(idx_adotante)
            self.repo.salvar_adotantes(self.adotantes)
            print(f"🗑️ Adotante '{removido.nome}' removido com sucesso!")
        except (ValueError, AdocaoError) as e:
            print(f"❌ Erro: {e}")

    def editar_animal(self, idx_animal: int, novo_nome=None, nova_raca=None, novo_porte=None, novo_temperamento=None, extra_dado=None):
        try:
            animal = self.buscar_animal(idx_animal)
            if novo_nome: animal._nome = novo_nome
            if nova_raca: animal._raca = nova_raca
            if novo_porte: animal._porte = novo_porte
            if novo_temperamento: animal._temperamento = novo_temperamento
            
            if isinstance(animal, Cachorro) and extra_dado is not None:
                animal._precisa_passeio = extra_dado
            elif isinstance(animal, Gato) and extra_dado is not None:
                animal._independencia = extra_dado
            
            animal.adicionar_evento("Dados cadastrais editados manualmente.")
            self.repo.salvar_animais(self.animais)
            print(f"✏️ Dados de {animal.nome} atualizados com sucesso!")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def editar_adotante(self, idx_adotante: int, novo_nome=None, novo_contato=None, nova_moradia=None, nova_area=None, novas_criancas=None):
        try:
            adotante = self.buscar_adotante(idx_adotante)
            
            if novo_nome:
                adotante._nome = novo_nome
            if novo_contato:
                adotante._contato = novo_contato
            if nova_moradia:
                adotante._moradia = nova_moradia
            if nova_area:
                adotante._area_util = nova_area
            if novas_criancas is not None:
                adotante._tem_criancas = novas_criancas
            
            self.repo.salvar_adotantes(self.adotantes)
            print(f"✏️ Dados de {adotante.nome} atualizados com sucesso!")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def _buscar_por_indice(self, idx_animal: int, idx_adotante: Optional[int] = None) -> Tuple[Animal, Optional[Adotante]]:
        animal = self.buscar_animal(idx_animal)
        adotante = None
        if idx_adotante is not None:
            adotante = self.buscar_adotante(idx_adotante)
        return animal, adotante

    def _validar_politica_adocao(self, animal: Animal, adotante: Adotante):
        if adotante.idade < self.settings["idade_minima"]:
            raise PoliticaNaoAtendidaError(f"Adotante deve ter >= {self.settings['idade_minima']} anos.")

        if animal.porte == PorteAnimal.G:
            if adotante.moradia != TipoMoradia.CASA:
                raise PoliticaNaoAtendidaError("Animais de Porte Grande exigem moradia em CASA.")
            if adotante.area_util < self.settings["area_minima_g"]:
                raise PoliticaNaoAtendidaError(f"Porte G exige área mínima de {self.settings['area_minima_g']}m².")

        if adotante.tem_criancas:
            temperamentos_pet = [t.lower() for t in animal.temperamento]
            if "arisco" in temperamentos_pet or "agressivo" in temperamentos_pet:
                raise PoliticaNaoAtendidaError("Não permitido adotar animais 'ariscos' em casas com crianças.")

    def _calcular_compatibilidade(self, animal: Animal, adotante: Adotante) -> Tuple[int, List[str]]:
        score = 0
        detalhes = []
        pesos = self.settings["pesos_compatibilidade"]
        
        if (animal.porte == PorteAnimal.G and adotante.moradia == TipoMoradia.CASA) or animal.porte != PorteAnimal.G:
            score += pesos.get("moradia", 0)
            detalhes.append(f"[+] Moradia adequada (+{pesos['moradia']})")
        
        if not (adotante.tem_criancas and "arisco" in [t.lower() for t in animal.temperamento]):
            score += pesos.get("criancas", 0)
            detalhes.append(f"[+] Ambiente Seguro/Sem conflito (+{pesos['criancas']})")
            
        if adotante.idade > 30:
            score += pesos.get("experiencia", 0)
            detalhes.append(f"[+] Experiência presumida (+{pesos['experiencia']})")
        
        score += pesos.get("idade_energia", 0)
        
        return min(score, 100), detalhes

    def reservar_animal(self, idx_animal: int, idx_adotante: int):
        try:
            animal, adotante = self._buscar_por_indice(idx_animal, idx_adotante)
            
            if animal.status == StatusAnimal.RESERVADO:
                if animal.nome_reservante == adotante.nome:
                    raise ReservaInvalidaError(f"{adotante.nome}, você JÁ possui a reserva deste animal!")

                print(f"❌ {animal.nome} já está RESERVADO para {animal.nome_reservante}.")
                entrar = input("Deseja entrar na fila de espera? (s/n): ").lower()
                if entrar == 's':
                    self.entrar_fila_espera(idx_animal, idx_adotante)
                return
            
            if animal.status != StatusAnimal.DISPONIVEL:
                raise TransicaoStatusError(f"{animal.nome} não está disponível (Status: {animal.status.value}).")
            
            self._validar_politica_adocao(animal, adotante)

            animal.mudar_status(StatusAnimal.RESERVADO)
            animal.data_reserva = datetime.now().isoformat()
            animal.nome_reservante = adotante.nome
            
            self.repo.salvar_animais(self.animais)
            print(f"🗓️  Reserva confirmada para {adotante.nome}!")
            print(f"⚠️  Válida por {self.settings['reserva_horas']} horas.")
            
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def realizar_adocao(self, idx_animal: int, idx_adotante: int):
        try:
            animal, adotante = self._buscar_por_indice(idx_animal, idx_adotante)

            if animal.status == StatusAnimal.RESERVADO and animal.nome_reservante != adotante.nome:
                raise ReservaInvalidaError(f"Este animal está reservado para {animal.nome_reservante}.")

            if animal.status not in [StatusAnimal.DISPONIVEL, StatusAnimal.RESERVADO]:
                raise TransicaoStatusError(f"Status inválido ({animal.status.value}).")

            self._validar_politica_adocao(animal, adotante)

            estrategia = FabricaTaxas.obter_estrategia(animal, adotante)
            valor_taxa = estrategia.calcular(animal, adotante)

            animal.mudar_status(StatusAnimal.ADOTADO)
            self.repo.salvar_animais(self.animais)
            
            try:
                valor_float = float(valor_taxa)
                texto_taxa = f"R$ {valor_float:.2f}"
            except:
                texto_taxa = f"R$ {valor_taxa}"

            self.notificar_observadores(f"ADOÇÃO: {adotante.nome} adotou {animal.nome}. Taxa: {texto_taxa}")

            print(f"🎉 ADOÇÃO SUCESSO! {adotante.nome} adotou {animal.nome}!")
            print("="*40)
            print("          RECIBO DE ADOÇÃO")
            print("="*40)
            print(f"Animal: {animal.nome} ({animal.porte.value})")
            print(f"Tutor:  {adotante.nome}")
            print(f"Taxa:   {texto_taxa}")
            print("="*40)

        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def processar_devolucao(self, idx_animal: int, motivo: str):
        try:
            animal = self.buscar_animal(idx_animal)
            if animal.status != StatusAnimal.ADOTADO:
                raise TransicaoStatusError("Apenas animais adotados podem ser devolvidos.")

            print(f"📝 Motivo registrado: '{motivo}'")
            animal.mudar_status(StatusAnimal.DEVOLVIDO)

            motivo_lower = motivo.lower()
            palavras_saude = ["doente", "saude", "saúde", "doença", "vômito", "ferido"]
            palavras_agressao = ["mordeu", "agressivo", "atacou", "bravo", "arisco"]

            eh_saude = any(p in motivo_lower for p in palavras_saude)
            eh_agressao = any(p in motivo_lower for p in palavras_agressao)

            if eh_saude:
                animal.mudar_status(StatusAnimal.QUARENTENA)
            elif eh_agressao:
                animal.mudar_status(StatusAnimal.INADOTAVEL)
            else:
                animal.mudar_status(StatusAnimal.DISPONIVEL)

            self.repo.salvar_animais(self.animais)
            print(f"🔙 Devolução concluída. Novo status: {animal.status.value}.")
            
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def entrar_fila_espera(self, idx_animal: int, idx_adotante: int):
        try:
            animal, adotante = self._buscar_por_indice(idx_animal, idx_adotante)
            if animal.nome_reservante == adotante.nome:
                raise ReservaInvalidaError(f"{adotante.nome}, você já é o titular da reserva!")
            self._validar_politica_adocao(animal, adotante)

            score, detalhes = self._calcular_compatibilidade(animal, adotante)
            animal.fila_espera.adicionar(adotante, score)
            animal.adicionar_evento(f"{adotante.nome} entrou na fila (Score: {score}).")
            self.repo.salvar_animais(self.animais)
            
            print(f"✅ {adotante.nome} entrou na fila com Score {score}/100.")
            for d in detalhes: print("   " + d)
            
            posicao = 0
            for i, item in enumerate(animal.fila_espera.interessados):
                if item['adotante'].nome == adotante.nome:
                    posicao = i + 1
                    break
            
            if posicao == 0: print("⚠️ Aviso: Adotante já estava na fila.")
            else: print(f"📍 Posição atual: {posicao}º lugar")

        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def processar_reservas_vencidas(self):
        print("🔄 Verificando validade das reservas...")
        agora = datetime.now()
        horas_limite = self.settings["reserva_horas"]
        alterou = False

        for animal in self.animais:
            if animal.status == StatusAnimal.RESERVADO and animal.data_reserva:
                data_res = datetime.fromisoformat(animal.data_reserva)
                horas_passadas = (agora - data_res).total_seconds() / 3600

                if horas_passadas > horas_limite:
                    old_dono = animal.nome_reservante
                    print(f"⏰ Reserva de {old_dono} p/ {animal.nome} VENCEU ({horas_passadas:.1f}h passadas).")
                    
                    proximo_adotante = animal.fila_espera.proximo()
                    if proximo_adotante:
                        animal.nome_reservante = proximo_adotante.nome
                        animal.data_reserva = agora.isoformat()
                        print(f"🔔 VEZ DA FILA: {animal.nome} agora reservado para {proximo_adotante.nome}!")
                        animal.adicionar_evento(f"Reserva expirada. Transferida p/ fila: {proximo_adotante.nome}")
                    else:
                        animal.mudar_status(StatusAnimal.DISPONIVEL)
                        print(f"🔓 {animal.nome} está DISPONÍVEL novamente.")
                        animal.adicionar_evento("Reserva expirada. Animal liberado.")
                    alterou = True

                self.notificar_observadores(f"EXPIRAÇÃO: Reserva de {animal.nome} (Tutor: {old_dono}) venceu e foi cancelada.")
        
        if alterou:
            self.repo.salvar_animais(self.animais)
            print("✅ Processamento concluído e dados salvos.")
        else:
            print("✅ Nenhuma reserva vencida encontrada.")

    def visualizar_detalhes_fila(self, idx_animal: int):
        try:
            animal = self.buscar_animal(idx_animal)
            print(f"\n📊 DETALHES DE: {animal.nome}")
            print(f"Status Atual: {animal.status.value}")
            
            if animal.status == StatusAnimal.RESERVADO and animal.data_reserva:
                dt = datetime.fromisoformat(animal.data_reserva)
                expira_em = dt + timedelta(hours=self.settings["reserva_horas"])
                restante = expira_em - datetime.now()
                str_restante = str(restante).split('.')[0]
                if restante.total_seconds() < 0: str_restante = "VENCIDO"
                print(f"👑 Titular da Reserva: {animal.nome_reservante}")
                print(f"⏳ Vencimento em: {str_restante}")
            
            print(f"\n👥 FILA DE ESPERA ({len(animal.fila_espera)} interessados):")
            if len(animal.fila_espera) == 0: print("   (Vazia)")
            else:
                for i, item in enumerate(animal.fila_espera.interessados):
                    adotante = item['adotante']
                    score = item['score']
                    dt_entr = item['data_entrada'].split('T')[0]
                    print(f"   {i+1}º. {adotante.nome} | Score: {score} | Desde: {dt_entr}")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def vacinar_animal(self, idx_animal: int, nome_vacina: str):
        try:
            animal = self.buscar_animal(idx_animal)
            if hasattr(animal, 'vacinar'):
                animal.vacinar(nome_vacina)
                self.repo.salvar_animais(self.animais)
                print(f"💉 {animal.nome} foi vacinado contra {nome_vacina}!")
            else: print(f"⚠️ {animal.nome} não pode ser vacinado.")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def treinar_animal(self, idx_animal: int):
        try:
            animal = self.buscar_animal(idx_animal)
            if hasattr(animal, 'treinar'):
                animal.treinar()
                self.repo.salvar_animais(self.animais)
                print(f"🎓 {animal.nome} recebeu treinamento! Nível atualizado.")
            else: print(f"⚠️ {animal.nome} não pode ser treinado.")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def gerar_relatorio_animais(self, apenas_adotados=False):
        print("\n--- STATUS DO ABRIGO ---")
        contador = 0
        for i, a in enumerate(self.animais):
            if apenas_adotados and a.status != StatusAnimal.ADOTADO:
                continue
                
            extra_info = ""
            if a.status == StatusAnimal.RESERVADO:
                extra_info = f" [Reservado: {a.nome_reservante}]"
            if len(a.fila_espera) > 0:
                extra_info += f" [Fila: {len(a.fila_espera)}]"
            icone = "🟢" if a.status == StatusAnimal.DISPONIVEL else "🔴" if a.status == StatusAnimal.ADOTADO else "🟡"
            print(f"[{i}] {icone} {a.nome} ({a.porte.value}) - {a.status.value}{extra_info}")
            contador += 1
        
        if contador == 0:
            print("   (Nenhum animal encontrado para este filtro)")

    def listar_adotantes(self):
        print("\n--- ADOTANTES ---")
        for i, a in enumerate(self.adotantes):
            aviso = ""
            if a.idade < self.settings["idade_minima"]:
                aviso = " ⚠️ [Menor de Idade - Adoção Bloqueada]"
            print(f"[{i}] {a.nome}, {a.idade} anos ({a.moradia.value}, {a.area_util}m²){aviso}")

    def gerar_relatorios_estatisticos(self):
        linhas_relatorio = []
        def log(texto):
            print(texto)
            linhas_relatorio.append(texto)

        log("\n" + "="*50)
        log("📊 RELATÓRIOS ESTATÍSTICOS DO ABRIGO")
        log("Data de Geração: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        log("="*50)

        log("\n🏆 TOP 5 - ANIMAIS MAIS POPULARES (Maiores Filas)")
        populares = [(a, len(a.fila_espera)) for a in self.animais if len(a.fila_espera) > 0]
        populares.sort(key=lambda x: x[1], reverse=True)
        if not populares: log("   (Nenhum animal com fila de espera no momento)")
        else:
            for i, (animal, tamanho) in enumerate(populares[:5]):
                log(f"   {i+1}º. {animal.nome} - Fila: {tamanho} pessoas")

        log("\n📈 TAXA DE ADOÇÃO POR ESPÉCIE")
        stats_caes = self._calcular_taxa_adocao_por_tipo(Cachorro)
        stats_gatos = self._calcular_taxa_adocao_por_tipo(Gato)
        log(f"   🐶 Cães:  {stats_caes['adotados']}/{stats_caes['total']} ({stats_caes['taxa']}%)")
        log(f"   🐱 Gatos: {stats_gatos['adotados']}/{stats_gatos['total']} ({stats_gatos['taxa']}%)")

        log("\n⏱️  TEMPO MÉDIO ATÉ A ADOÇÃO")
        media_dias = self._calcular_tempo_medio_adocao()
        if media_dias is not None: log(f"   Média geral: {media_dias:.1f} dias")
        else: log("   (Dados insuficientes para cálculo)")

        log("\n⚠️  DEVOLUÇÕES E ANIMAIS INADOTÁVEIS")
        quarentena = len([a for a in self.animais if a.status == StatusAnimal.QUARENTENA])
        inadotavel = len([a for a in self.animais if a.status == StatusAnimal.INADOTAVEL])
        devolvidos = len([a for a in self.animais if a.status == StatusAnimal.DEVOLVIDO])
        log(f"   🏥 Em Quarentena (Saúde): {quarentena}")
        log(f"   ⛔ Inadotáveis (Comportamento): {inadotavel}")
        log(f"   🔙 Devolvidos (Aguardando): {devolvidos}")
        log("="*50)

        try:
            pasta_relatorios = "relatorios"
            if not os.path.exists(pasta_relatorios): os.makedirs(pasta_relatorios)
            nome_arquivo = f"relatorio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            caminho_completo = os.path.join(pasta_relatorios, nome_arquivo)
            with open(caminho_completo, "w", encoding="utf-8") as arquivo:
                arquivo.write("\n".join(linhas_relatorio))
            print(f"\n💾 Relatório salvo com sucesso em: {caminho_completo}")
        except Exception as e: print(f"\n❌ Erro ao salvar arquivo de relatório: {e}")

    def _calcular_taxa_adocao_por_tipo(self, classe_tipo):
        total = 0
        adotados = 0
        for animal in self.animais:
            if isinstance(animal, classe_tipo):
                total += 1
                if animal.status == StatusAnimal.ADOTADO: adotados += 1
        taxa = (adotados / total * 100) if total > 0 else 0.0
        return {"total": total, "adotados": adotados, "taxa": round(taxa, 1)}

    def _calcular_tempo_medio_adocao(self) -> Optional[float]:
        total_dias = 0
        count = 0
        for animal in self.animais:
            if animal.status == StatusAnimal.ADOTADO:
                data_entrada = None
                data_adocao = None
                for evento in animal.historico_eventos:
                    if "Cadastrado" in evento:
                        try:
                            data_str = evento.split(']')[0].replace('[', '')
                            data_entrada = datetime.strptime(data_str, "%Y-%m-%d %H:%M")
                        except: pass
                    if "Status alterado: Reservado -> Adotado" in evento or "Status alterado: Disponível -> Adotado" in evento:
                        try:
                            data_str = evento.split(']')[0].replace('[', '')
                            data_adocao = datetime.strptime(data_str, "%Y-%m-%d %H:%M")
                        except: pass
                if data_entrada and data_adocao:
                    diferenca = data_adocao - data_entrada
                    total_dias += diferenca.total_seconds() / 86400 
                    count += 1
        if count == 0: return None
        return total_dias / count
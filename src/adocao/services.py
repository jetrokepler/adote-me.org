import json
import os
from typing import List, Tuple, Optional, Dict, Any, Type
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
    """Interface abstrata para observadores do sistema (Observer Pattern)."""

    @abstractmethod
    def atualizar(self, mensagem: str) -> None:
        """Método chamado quando um evento ocorre no sujeito observado.

        Args:
            mensagem (str): A mensagem ou descrição do evento.
        """
        pass

class LoggerObserver(Observador):
    """Implementação concreta de Observador que registra eventos em um arquivo de log.

    Attributes:
        arquivo (str): Nome do arquivo de log.
    """

    def __init__(self, arquivo: str = "historico_eventos.log") -> None:
        """Inicializa o LoggerObserver.

        Args:
            arquivo (str, optional): Caminho do arquivo de log. Defaults to "historico_eventos.log".
        """
        self.arquivo = arquivo

    def atualizar(self, mensagem: str) -> None:
        """Escreve a mensagem formatada com timestamp no arquivo de log.

        Args:
            mensagem (str): A mensagem do evento a ser logada.
        """
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
    """Classe principal (Fachada/Controller) que gerencia o sistema de adoção.

    Responsável por coordenar repositórios, regras de negócio, configurações
    e notificações de eventos.

    Attributes:
        settings (Dict[str, Any]): Configurações do sistema carregadas.
        repo (Repositorio): Instância do repositório (SQLite ou JSON).
        animais (List[Animal]): Lista de animais carregados em memória.
        adotantes (List[Adotante]): Lista de adotantes carregados em memória.
        observadores (List[Observador]): Lista de observadores registrados.
    """

    def __init__(self) -> None:
        """Inicializa o sistema, carrega configurações e repositórios."""
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

    def adicionar_observador(self, observador: Observador) -> None:
        """Registra um novo observador para receber notificações.

        Args:
            observador (Observador): Instância do observador a ser registrada.
        """
        self.observadores.append(observador)

    def notificar_observadores(self, evento: str) -> None:
        """Notifica todos os observadores registrados sobre um evento.

        Args:
            evento (str): Descrição do evento ocorrido.
        """
        for obs in self.observadores:
            obs.atualizar(evento)

    def _carregar_settings(self) -> Dict[str, Any]:
        """Carrega as configurações do arquivo JSON ou cria o padrão se não existir.

        Returns:
            Dict[str, Any]: Dicionário contendo as configurações do sistema.
        """
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

    def _salvar_settings_arquivo(self, dados: Dict[str, Any]) -> None:
        """Salva as configurações no arquivo settings.json.

        Args:
            dados (Dict[str, Any]): Dicionário de configurações a ser salvo.
        """
        try:
            with open("settings.json", "w", encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar settings: {e}")

    def atualizar_configuracao(self, chave: str, novo_valor: Any) -> Tuple[bool, str]:
        """Atualiza uma chave específica nas configurações do sistema.

        Args:
            chave (str): A chave de configuração a ser alterada.
            novo_valor (Any): O novo valor a ser atribuído.

        Returns:
            Tuple[bool, str]: (Sucesso, Mensagem de retorno).
        """
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
        """Busca um animal pelo índice na lista em memória.

        Args:
            idx (int): Índice do animal.

        Returns:
            Animal: O objeto animal encontrado.

        Raises:
            EntidadeNaoEncontradaError: Se o índice for inválido.
        """
        try:
            return self.animais[idx]
        except IndexError:
            raise EntidadeNaoEncontradaError(f"Animal com índice {idx} não encontrado.")

    def buscar_adotante(self, idx: int) -> Adotante:
        """Busca um adotante pelo índice na lista em memória.

        Args:
            idx (int): Índice do adotante.

        Returns:
            Adotante: O objeto adotante encontrado.

        Raises:
            EntidadeNaoEncontradaError: Se o índice for inválido.
        """
        try:
            return self.adotantes[idx]
        except IndexError:
            raise EntidadeNaoEncontradaError(f"Adotante com índice {idx} não encontrado.")

    def cadastrar_cachorro(self, nome: str, raca: str, porte: PorteAnimal, temperamento: List[str], precisa_passeio: bool) -> None:
        """Cadastra um novo cachorro no sistema e salva no repositório.

        Args:
            nome (str): Nome do cachorro.
            raca (str): Raça do cachorro.
            porte (PorteAnimal): Porte do animal.
            temperamento (List[str]): Lista de temperamentos.
            precisa_passeio (bool): Se necessita de passeio.
        """
        novo_pet = Cachorro(nome, raca, StatusAnimal.DISPONIVEL, porte, temperamento, precisa_passeio)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Cachorro {nome} cadastrado com sucesso!")

    def cadastrar_gato(self, nome: str, raca: str, porte: PorteAnimal, temperamento: List[str], independencia: int) -> None:
        """Cadastra um novo gato no sistema e salva no repositório.

        Args:
            nome (str): Nome do gato.
            raca (str): Raça do gato.
            porte (PorteAnimal): Porte do animal.
            temperamento (List[str]): Lista de temperamentos.
            independencia (int): Nível de independência.
        """
        novo_pet = Gato(nome, raca, StatusAnimal.DISPONIVEL, porte, temperamento, independencia)
        self.animais.append(novo_pet)
        self.repo.salvar_animais(self.animais)
        print(f"✅ Gato {nome} cadastrado com sucesso!")

    def cadastrar_adotante(self, nome: str, contato: str, idade: int, moradia: TipoMoradia, area_util: float, tem_criancas: bool) -> None:
        """Cadastra um novo adotante no sistema e salva no repositório.

        Args:
            nome (str): Nome do adotante.
            contato (str): Contato.
            idade (int): Idade.
            moradia (TipoMoradia): Tipo de moradia.
            area_util (float): Área útil em m².
            tem_criancas (bool): Se possui crianças.
        """
        novo_adotante = Adotante(nome, contato, idade, moradia, area_util, tem_criancas)
        self.adotantes.append(novo_adotante)
        self.repo.salvar_adotantes(self.adotantes)
        print(f"👤 Adotante {nome} cadastrado com sucesso!")

    def excluir_animal(self, idx_animal: int) -> None:
        """Remove um animal do sistema pelo índice.

        Args:
            idx_animal (int): Índice do animal a ser removido.
        """
        try:
            self.buscar_animal(idx_animal)
            removido = self.animais.pop(idx_animal)
            self.repo.salvar_animais(self.animais)
            print(f"🗑️ Animal '{removido.nome}' removido com sucesso!")
        except (ValueError, AdocaoError) as e:
            print(f"❌ Índice inválido ou erro: {e}")

    def excluir_adotante(self, idx_adotante: int) -> None:
        """Remove um adotante do sistema pelo índice.

        Args:
            idx_adotante (int): Índice do adotante a ser removido.
        """
        try:
            self.buscar_adotante(idx_adotante)
            removido = self.adotantes.pop(idx_adotante)
            self.repo.salvar_adotantes(self.adotantes)
            print(f"🗑️ Adotante '{removido.nome}' removido com sucesso!")
        except (ValueError, AdocaoError) as e:
            print(f"❌ Erro: {e}")

    def editar_animal(self, idx_animal: int, novo_nome: Optional[str] = None, nova_raca: Optional[str] = None, novo_porte: Optional[PorteAnimal] = None, novo_temperamento: Optional[List[str]] = None, extra_dado: Any = None) -> None:
        """Edita os dados de um animal existente.

        Args:
            idx_animal (int): Índice do animal.
            novo_nome (Optional[str], optional): Novo nome. Defaults to None.
            nova_raca (Optional[str], optional): Nova raça. Defaults to None.
            novo_porte (Optional[PorteAnimal], optional): Novo porte. Defaults to None.
            novo_temperamento (Optional[List[str]], optional): Novo temperamento. Defaults to None.
            extra_dado (Any, optional): Dado específico (passeio para Cães, independência para Gatos). Defaults to None.
        """
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

    def editar_adotante(self, idx_adotante: int, novo_nome: Optional[str] = None, novo_contato: Optional[str] = None, nova_moradia: Optional[TipoMoradia] = None, nova_area: Optional[float] = None, novas_criancas: Optional[bool] = None) -> None:
        """Edita os dados de um adotante existente.

        Args:
            idx_adotante (int): Índice do adotante.
            novo_nome (Optional[str], optional): Novo nome. Defaults to None.
            novo_contato (Optional[str], optional): Novo contato. Defaults to None.
            nova_moradia (Optional[TipoMoradia], optional): Nova moradia. Defaults to None.
            nova_area (Optional[float], optional): Nova área útil. Defaults to None.
            novas_criancas (Optional[bool], optional): Novo status de crianças. Defaults to None.
        """
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
        """Método auxiliar para recuperar objetos pelos índices.

        Args:
            idx_animal (int): Índice do animal.
            idx_adotante (Optional[int], optional): Índice do adotante. Defaults to None.

        Returns:
            Tuple[Animal, Optional[Adotante]]: Tupla contendo os objetos encontrados.
        """
        animal = self.buscar_animal(idx_animal)
        adotante = None
        if idx_adotante is not None:
            adotante = self.buscar_adotante(idx_adotante)
        return animal, adotante

    def _validar_politica_adocao(self, animal: Animal, adotante: Adotante) -> None:
        """Verifica se o adotante cumpre os requisitos para adotar o animal.

        Args:
            animal (Animal): O animal pretendido.
            adotante (Adotante): O candidato à adoção.

        Raises:
            PoliticaNaoAtendidaError: Se algum critério (idade, moradia, segurança) não for atendido.
        """
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
        """Calcula um score de compatibilidade entre adotante e animal.

        Args:
            animal (Animal): O animal.
            adotante (Adotante): O adotante.

        Returns:
            Tuple[int, List[str]]: Score (0-100) e lista de detalhes da pontuação.
        """
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

    def reservar_animal(self, idx_animal: int, idx_adotante: int) -> None:
        """Tenta reservar um animal para um adotante ou sugere entrar na fila.

        Args:
            idx_animal (int): Índice do animal.
            idx_adotante (int): Índice do adotante.
        """
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

    def realizar_adocao(self, idx_animal: int, idx_adotante: int) -> None:
        """Efetiva a adoção de um animal, calculando taxas e atualizando status.

        Args:
            idx_animal (int): Índice do animal.
            idx_adotante (int): Índice do adotante.
        """
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

    def processar_devolucao(self, idx_animal: int, motivo: str) -> None:
        """Processa a devolução de um animal adotado, definindo o novo status.

        Args:
            idx_animal (int): Índice do animal.
            motivo (str): Motivo da devolução.
        """
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

    def entrar_fila_espera(self, idx_animal: int, idx_adotante: int) -> None:
        """Adiciona um adotante à fila de espera de um animal.

        Args:
            idx_animal (int): Índice do animal.
            idx_adotante (int): Índice do adotante.
        """
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

    def processar_reservas_vencidas(self) -> None:
        """Verifica reservas que excederam o tempo limite e passa para o próximo da fila."""
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

    def visualizar_detalhes_fila(self, idx_animal: int) -> None:
        """Exibe detalhes da reserva atual e da fila de espera de um animal.

        Args:
            idx_animal (int): Índice do animal.
        """
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

    def vacinar_animal(self, idx_animal: int, nome_vacina: str) -> None:
        """Aplica vacina em um animal, se a classe dele suportar.

        Args:
            idx_animal (int): Índice do animal.
            nome_vacina (str): Nome da vacina.
        """
        try:
            animal = self.buscar_animal(idx_animal)
            if hasattr(animal, 'vacinar'):
                animal.vacinar(nome_vacina)
                self.repo.salvar_animais(self.animais)
                print(f"💉 {animal.nome} foi vacinado contra {nome_vacina}!")
            else: print(f"⚠️ {animal.nome} não pode ser vacinado.")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def treinar_animal(self, idx_animal: int) -> None:
        """Aplica treinamento em um animal, se a classe dele suportar.

        Args:
            idx_animal (int): Índice do animal.
        """
        try:
            animal = self.buscar_animal(idx_animal)
            if hasattr(animal, 'treinar'):
                animal.treinar()
                self.repo.salvar_animais(self.animais)
                print(f"🎓 {animal.nome} recebeu treinamento! Nível atualizado.")
            else: print(f"⚠️ {animal.nome} não pode ser treinado.")
        except (ValueError, AdocaoError) as e: print(f"❌ {e}")

    def gerar_relatorio_animais(self, apenas_adotados: bool = False) -> None:
        """Gera um relatório impresso no console com o status dos animais.

        Args:
            apenas_adotados (bool, optional): Filtra apenas os adotados. Defaults to False.
        """
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

    def listar_adotantes(self) -> None:
        """Imprime a lista de adotantes cadastrados com alertas de elegibilidade."""
        print("\n--- ADOTANTES ---")
        for i, a in enumerate(self.adotantes):
            aviso = ""
            if a.idade < self.settings["idade_minima"]:
                aviso = " ⚠️ [Menor de Idade - Adoção Bloqueada]"
            print(f"[{i}] {a.nome}, {a.idade} anos ({a.moradia.value}, {a.area_util}m²){aviso}")

    def gerar_relatorios_estatisticos(self) -> None:
        """Gera relatórios estatísticos detalhados e salva em arquivo .txt."""
        linhas_relatorio = []
        def log(texto: str) -> None:
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

    def _calcular_taxa_adocao_por_tipo(self, classe_tipo: Type[Animal]) -> Dict[str, Any]:
        """Calcula estatísticas de adoção para uma classe de animal específica.

        Args:
            classe_tipo (Type[Animal]): A classe (Cachorro ou Gato) para filtrar.

        Returns:
            Dict[str, Any]: Dicionário com total, adotados e taxa percentual.
        """
        total = 0
        adotados = 0
        for animal in self.animais:
            if isinstance(animal, classe_tipo):
                total += 1
                if animal.status == StatusAnimal.ADOTADO: adotados += 1
        taxa = (adotados / total * 100) if total > 0 else 0.0
        return {"total": total, "adotados": adotados, "taxa": round(taxa, 1)}

    def _calcular_tempo_medio_adocao(self) -> Optional[float]:
        """Calcula o tempo médio entre cadastro e adoção baseado no histórico.

        Returns:
            Optional[float]: Média de dias ou None se não houver dados.
        """
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
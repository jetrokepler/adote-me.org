class AdocaoError(Exception):
    """Classe base para todas as exceções do sistema de adoção."""
    pass

class RepositorioError(AdocaoError):
    """Erros relacionados a leitura/escrita de arquivos."""
    pass

class EntidadeNaoEncontradaError(AdocaoError):
    """Quando se busca um ID que não existe."""
    pass

class RegraNegocioError(AdocaoError):
    """Classe pai para erros de violação de regras de negócio."""
    pass

class PoliticaNaoAtendidaError(RegraNegocioError):
    """
    Ex: Adotante menor de idade, 
    Apartamento para cão grande, etc.
    (Baseado na sua imagem: PoliticaNaoAtendidaError)
    """
    pass

class TransicaoStatusError(RegraNegocioError):
    """
    Ex: Tentar devolver um animal que nem foi adotado.
    (Baseado na sua imagem: TransicaoDeEstadoInvalidaError)
    """
    pass

class ReservaInvalidaError(RegraNegocioError):
    """
    Ex: Tentar reservar um animal que já está reservado para outro.
    (Baseado na sua imagem: ReservaInvalidaError)
    """
    pass
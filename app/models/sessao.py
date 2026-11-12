import secrets
import time


TEMPO_EXPIRACAO_SESSAO = 3600


class Sessao:
    """Guarda os dados e o prazo de validade de uma sessão."""

    def __init__(self, token, username, expira_em):
        self.token = token
        self.username = username
        self.expira_em = expira_em


class GerenciadorSessoes:
    """Cria, consulta e encerra as sessões durante a execução."""

    def __init__(self, duracao=TEMPO_EXPIRACAO_SESSAO):
        self.sessoes = {}
        self.duracao = duracao

    def criar(self, username):
        token = secrets.token_urlsafe(32)
        expira_em = time.monotonic() + self.duracao
        self.sessoes[token] = Sessao(token, username, expira_em)
        return token

    def usuario(self, token):
        sessao = self.sessoes.get(token)
        if not sessao:
            return None

        if time.monotonic() >= sessao.expira_em:
            self.encerrar(token)
            return None

        return sessao.username

    def encerrar(self, token):
        if token:
            self.sessoes.pop(token, None)

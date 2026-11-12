from pathlib import Path

from bottle import TEMPLATE_PATH, template

from app.controllers.datarecord import ComponentRecord, UserRecord
from app.models.sessao import GerenciadorSessoes

VIEWS_DIR = Path(__file__).resolve().parent.parent / "views" / "html"
if str(VIEWS_DIR) not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, str(VIEWS_DIR))


class Application:
    """Reúne as operações usadas pelas páginas do sistema."""

    def __init__(self):
        self.users = UserRecord()
        self.componentes = ComponentRecord()
        self.sessoes = GerenciadorSessoes()

    def autenticar(self, username, password):
        user = self.users.buscar(username)
        if user and user.confere_senha(password):
            return self.sessoes.criar(user.username)
        return None

    def usuario_logado(self, token):
        return self.sessoes.usuario(token)

    def logout(self, token):
        self.sessoes.encerrar(token)

    def render_portal(self, erro=None):
        return template("portal", erro=erro)

    def render_banco(self, username):
        componentes = self.componentes.listar()
        quantidade_total = sum(item.quantidade for item in componentes)
        return template(
            "banco",
            username=username,
            componentes=componentes,
            quantidade_total=quantidade_total,
        )

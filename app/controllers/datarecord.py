import json
import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

from app.models.componente import Componente
from app.models.user_account import User_account

DB_DIR = Path(__file__).resolve().parent / "db"


class DataRecord(ABC):
    """Classe base para ler e gravar objetos em arquivos JSON."""

    def __init__(self, filename):
        self.path = DB_DIR / filename
        self.models = []
        self.read()

    @abstractmethod
    def converter(self, data):
        """Transforma um registro do JSON no objeto correspondente."""
        raise NotImplementedError

    def read(self):
        if not self.path.exists():
            self.models = []
            return
        try:
            with self.path.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError(f"O arquivo {self.path.name} deve conter uma lista JSON.")
            self.models = [self.converter(item) for item in dados]
        except json.JSONDecodeError as exc:
            raise ValueError(f"O arquivo {self.path.name} contém JSON inválido.") from exc

    def save(self):
        DB_DIR.mkdir(parents=True, exist_ok=True)
        conteudo = [modelo.to_dict() for modelo in self.models]
        arquivo_temporario = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=DB_DIR, delete=False, suffix=".tmp"
            ) as arquivo:
                json.dump(conteudo, arquivo, ensure_ascii=False, indent=2)
                arquivo.write("\n")
                arquivo_temporario = arquivo.name
            os.replace(arquivo_temporario, self.path)
        finally:
            if arquivo_temporario and os.path.exists(arquivo_temporario):
                os.remove(arquivo_temporario)


class UserRecord(DataRecord):
    """Carrega e procura as contas usadas no portal."""

    def __init__(self):
        super().__init__("user_accounts.json")
        if not self.path.exists():
            username = os.getenv("TECHSTOCK_ADMIN_USER", "admin")
            password = os.getenv("TECHSTOCK_ADMIN_PASSWORD", "techstock123")
            self.models = [User_account.criar(username, password)]
            self.save()

    def converter(self, data):
        return User_account.from_dict(data)

    def buscar(self, username):
        username = (username or "").strip()
        return next((user for user in self.models if user.username == username), None)


class ComponentRecord(DataRecord):
    """Guarda os componentes e faz as operações do CRUD."""

    def __init__(self):
        super().__init__("componentes.json")
        if not self.path.exists():
            self.models = [
                Componente(1, "Resistor 220 Ω", "Resistor", 50, "Resistor de 1/4 W."),
                Componente(2, "Capacitor 100 µF", "Capacitor", 20, "Capacitor eletrolítico de 25 V."),
                Componente(3, "ESP32 DevKit", "Microcontrolador", 5, "Placa de desenvolvimento com Wi-Fi e Bluetooth."),
            ]
            self.save()

    def converter(self, data):
        return Componente.from_dict(data)

    def listar(self):
        return sorted(self.models, key=lambda componente: componente.id)

    def buscar(self, componente_id):
        componente_id = Componente.validar_id(componente_id)
        return next((item for item in self.models if item.id == componente_id), None)

    def criar(self, nome, categoria, quantidade, descricao=""):
        proximo_id = max((item.id for item in self.models), default=0) + 1
        novo = Componente(proximo_id, nome, categoria, quantidade, descricao)
        self.models.append(novo)
        self.save()
        return novo

    def atualizar(self, componente_id, nome=None, categoria=None, quantidade=None, descricao=None):
        componente = self.buscar(componente_id)
        if componente is None:
            return None
        componente.atualizar(nome, categoria, quantidade, descricao)
        self.save()
        return componente

    def remover(self, componente_id):
        componente = self.buscar(componente_id)
        if componente is None:
            return None
        self.models.remove(componente)
        self.save()
        return componente

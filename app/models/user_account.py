import hashlib
import hmac
import secrets


class User_account:
    """Armazena os dados da conta usada no login.

    A senha fica salva como hash com salt, não em texto puro.
    """

    ITERATIONS = 260_000

    def __init__(self, username, salt, password_hash):
        self.username = username
        self.salt = salt
        self.password_hash = password_hash

    @classmethod
    def criar(cls, username, password):
        username = (username or "").strip()
        if not username:
            raise ValueError("O nome de usuário não pode ficar vazio.")
        if not password:
            raise ValueError("A senha não pode ficar vazia.")

        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            cls.ITERATIONS,
        ).hex()
        return cls(username, salt, digest)

    def confere_senha(self, password):
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            (password or "").encode("utf-8"),
            self.salt.encode("utf-8"),
            self.ITERATIONS,
        ).hex()
        return hmac.compare_digest(self.password_hash, digest)

    def to_dict(self):
        return {
            "username": self.username,
            "salt": self.salt,
            "password_hash": self.password_hash,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["salt"], data["password_hash"])

    def __repr__(self):
        return f"User_account(username={self.username!r})"


UserAccount = User_account

class Componente:
    """Representa um item do catálogo."""

    def __init__(self, componente_id, nome, categoria, quantidade, descricao=""):
        self.id = self.validar_id(componente_id)
        self.nome = self.validar_texto(nome, "nome", 100)
        self.categoria = self.validar_texto(categoria, "categoria", 60)
        self.quantidade = self.validar_quantidade(quantidade)
        self.descricao = self.validar_descricao(descricao)

    @staticmethod
    def validar_id(valor):
        try:
            numero = int(valor)
        except (TypeError, ValueError):
            raise ValueError("O ID do componente deve ser um número inteiro.")
        if numero <= 0:
            raise ValueError("O ID do componente deve ser maior que zero.")
        return numero

    @staticmethod
    def validar_texto(valor, campo, limite):
        texto = (valor or "").strip()
        if not texto:
            raise ValueError(f"O campo {campo} é obrigatório.")
        if len(texto) > limite:
            raise ValueError(f"O campo {campo} deve ter no máximo {limite} caracteres.")
        return texto

    @staticmethod
    def validar_quantidade(valor):
        try:
            texto = str(valor).strip()
            if not texto or any(caractere in texto for caractere in (".", ",")):
                raise ValueError
            quantidade = int(texto)
        except (TypeError, ValueError):
            raise ValueError("A quantidade deve ser um número inteiro.")
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        return quantidade

    @staticmethod
    def validar_descricao(valor):
        descricao = (valor or "").strip()
        if len(descricao) > 300:
            raise ValueError("A descrição deve ter no máximo 300 caracteres.")
        return descricao

    def atualizar(self, nome=None, categoria=None, quantidade=None, descricao=None):
        novo_nome = self.nome if nome is None else self.validar_texto(nome, "nome", 100)
        nova_categoria = self.categoria if categoria is None else self.validar_texto(categoria, "categoria", 60)
        nova_quantidade = self.quantidade if quantidade is None else self.validar_quantidade(quantidade)
        nova_descricao = self.descricao if descricao is None else self.validar_descricao(descricao)

        self.nome = novo_nome
        self.categoria = nova_categoria
        self.quantidade = nova_quantidade
        self.descricao = nova_descricao

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "categoria": self.categoria,
            "quantidade": self.quantidade,
            "descricao": self.descricao,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["nome"],
            data["categoria"],
            data["quantidade"],
            data.get("descricao", ""),
        )

    def __repr__(self):
        return f"Componente(id={self.id}, nome={self.nome!r}, categoria={self.categoria!r})"

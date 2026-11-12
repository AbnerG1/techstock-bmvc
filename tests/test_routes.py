import json
import tempfile
import unittest
from http.cookies import SimpleCookie
from io import BytesIO
from pathlib import Path
from urllib.parse import urlencode
from wsgiref.util import setup_testing_defaults

from app.controllers import datarecord


class TestRotas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_original = datarecord.DB_DIR
        cls.pasta_inicial = tempfile.TemporaryDirectory()
        datarecord.DB_DIR = Path(cls.pasta_inicial.name)

        import route
        cls.route = route

    @classmethod
    def tearDownClass(cls):
        datarecord.DB_DIR = cls.db_original
        cls.pasta_inicial.cleanup()

    def setUp(self):
        self.pasta_teste = tempfile.TemporaryDirectory()
        datarecord.DB_DIR = Path(self.pasta_teste.name)
        self.route.application = self.route.Application()

    def tearDown(self):
        self.pasta_teste.cleanup()

    def requisicao(self, metodo, caminho, dados=None, cookie=None):
        corpo = urlencode(dados or {}).encode("utf-8")
        ambiente = {}
        setup_testing_defaults(ambiente)
        ambiente.update({
            "REQUEST_METHOD": metodo,
            "PATH_INFO": caminho,
            "QUERY_STRING": "",
            "SERVER_NAME": "localhost",
            "SERVER_PORT": "8080",
            "wsgi.url_scheme": "http",
            "wsgi.input": BytesIO(corpo),
            "CONTENT_LENGTH": str(len(corpo)),
        })

        if dados:
            ambiente["CONTENT_TYPE"] = "application/x-www-form-urlencoded"
        if cookie:
            ambiente["HTTP_COOKIE"] = cookie

        resultado = {}

        def iniciar_resposta(status, headers, exc_info=None):
            resultado["status"] = int(status.split(" ", 1)[0])
            resultado["headers"] = dict(headers)

        conteudo = b"".join(self.route.app(ambiente, iniciar_resposta))
        return resultado["status"], resultado["headers"], conteudo.decode("utf-8")

    def fazer_login(self):
        status, headers, _ = self.requisicao(
            "POST",
            "/portal",
            {"username": "admin", "password": "techstock123"},
        )
        self.assertIn(status, (302, 303, 307))
        cookie = SimpleCookie()
        cookie.load(headers["Set-Cookie"])
        return f"session_id={cookie['session_id'].value}"

    def test_login_correto_abre_a_pagina_banco(self):
        cookie = self.fazer_login()
        status, _, conteudo = self.requisicao("GET", "/banco", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertIn("Componentes cadastrados", conteudo)

    def test_login_incorreto_nao_autentica(self):
        status, _, _ = self.requisicao(
            "POST",
            "/portal",
            {"username": "admin", "password": "senha-errada"},
        )
        self.assertEqual(status, 401)

        status, _, _ = self.requisicao("GET", "/banco")
        self.assertIn(status, (302, 303, 307))

    def test_api_bloqueia_requisicao_sem_login(self):
        status, _, conteudo = self.requisicao(
            "POST",
            "/componentes",
            {
                "nome": "Sensor de teste",
                "categoria": "Sensor",
                "quantidade": "2",
            },
        )
        self.assertEqual(status, 401)
        self.assertIn("não autorizado", json.loads(conteudo)["erro"].lower())

    def test_api_rejeita_quantidade_invalida(self):
        cookie = self.fazer_login()
        status, _, conteudo = self.requisicao(
            "POST",
            "/componentes",
            {
                "nome": "Sensor de teste",
                "categoria": "Sensor",
                "quantidade": "-1",
            },
            cookie,
        )
        self.assertEqual(status, 400)
        self.assertIn("não pode ser negativa", json.loads(conteudo)["erro"])

    def test_crud_e_consulta_na_pagina_banco(self):
        cookie = self.fazer_login()

        status, _, resposta = self.requisicao(
            "POST",
            "/componentes",
            {
                "nome": "Sensor de teste",
                "categoria": "Sensor",
                "quantidade": "2",
                "descricao": "Registro usado no teste das rotas.",
            },
            cookie,
        )
        self.assertEqual(status, 201)
        componente_id = json.loads(resposta)["componente"]["id"]

        status, _, resposta = self.requisicao("GET", "/componentes", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertIn("Sensor de teste", resposta)

        status, _, conteudo = self.requisicao("GET", "/banco", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertIn("Sensor de teste", conteudo)

        status, _, _ = self.requisicao(
            "PUT",
            f"/componentes/{componente_id}",
            {"quantidade": "9"},
            cookie,
        )
        self.assertEqual(status, 200)

        status, _, conteudo = self.requisicao("GET", "/banco", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertIn("<strong>9</strong>", conteudo)

        status, _, _ = self.requisicao(
            "DELETE",
            f"/componentes/{componente_id}",
            cookie=cookie,
        )
        self.assertEqual(status, 200)

        status, _, conteudo = self.requisicao("GET", "/banco", cookie=cookie)
        self.assertEqual(status, 200)
        self.assertNotIn("Sensor de teste", conteudo)


if __name__ == "__main__":
    unittest.main()

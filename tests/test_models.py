import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.controllers.datarecord import ComponentRecord, DataRecord
from app.models.componente import Componente
from app.models.sessao import GerenciadorSessoes
from app.models.user_account import User_account


class TestComponente(unittest.TestCase):
    def test_cria_componente_valido(self):
        componente = Componente(1, "ESP32 DevKit", "Microcontrolador", "5", "Placa de desenvolvimento")
        self.assertEqual(componente.nome, "ESP32 DevKit")
        self.assertEqual(componente.categoria, "Microcontrolador")
        self.assertEqual(componente.quantidade, 5)

    def test_nome_obrigatorio(self):
        with self.assertRaises(ValueError):
            Componente(1, "", "Sensor", 2)

    def test_quantidade_nao_pode_ser_negativa(self):
        with self.assertRaises(ValueError):
            Componente(1, "Sensor", "Sensor", -1)

    def test_atualiza_campos(self):
        componente = Componente(1, "Resistor", "Resistor", 10)
        componente.atualizar(quantidade="25", descricao="Estoque atualizado")
        self.assertEqual(componente.quantidade, 25)
        self.assertEqual(componente.descricao, "Estoque atualizado")

    def test_atualizacao_invalida_nao_muda_os_dados(self):
        componente = Componente(1, "Resistor", "Resistor", 10, "Valor inicial")
        with self.assertRaises(ValueError):
            componente.atualizar(nome="Novo nome", quantidade="-1")
        self.assertEqual(componente.nome, "Resistor")
        self.assertEqual(componente.quantidade, 10)
        self.assertEqual(componente.descricao, "Valor inicial")


class TestUserAccount(unittest.TestCase):
    def test_senha_correta_e_incorreta(self):
        usuario = User_account.criar("abner", "senha-de-teste")
        self.assertTrue(usuario.confere_senha("senha-de-teste"))
        self.assertFalse(usuario.confere_senha("senha-errada"))

    def test_senha_nao_fica_em_texto_puro(self):
        usuario = User_account.criar("abner", "senha-de-teste")
        dados = usuario.to_dict()
        self.assertNotIn("senha-de-teste", str(dados))
        self.assertIn("password_hash", dados)
        self.assertIn("salt", dados)


class TestDataRecord(unittest.TestCase):
    def test_datarecord_e_abstrata(self):
        with self.assertRaises(TypeError):
            DataRecord("teste.json")


class TestGerenciadorSessoes(unittest.TestCase):
    def test_cria_consulta_e_encerra_sessao(self):
        sessoes = GerenciadorSessoes()
        token = sessoes.criar("abner")
        self.assertEqual(sessoes.usuario(token), "abner")
        sessoes.encerrar(token)
        self.assertIsNone(sessoes.usuario(token))

    def test_sessao_expira_apos_o_prazo(self):
        sessoes = GerenciadorSessoes(duracao=10)
        with patch("app.models.sessao.time.monotonic", return_value=100):
            token = sessoes.criar("abner")

        with patch("app.models.sessao.time.monotonic", return_value=109):
            self.assertEqual(sessoes.usuario(token), "abner")

        with patch("app.models.sessao.time.monotonic", return_value=110):
            self.assertIsNone(sessoes.usuario(token))

        self.assertNotIn(token, sessoes.sessoes)


class TestComponentRecord(unittest.TestCase):
    def test_crud_e_persistencia_json(self):
        with tempfile.TemporaryDirectory() as pasta_temporaria:
            with patch("app.controllers.datarecord.DB_DIR", Path(pasta_temporaria)):
                banco = ComponentRecord()
                self.assertEqual(len(banco.listar()), 3)

                criado = banco.criar("Sensor LDR", "Sensor", "12", "Sensor de luminosidade")
                self.assertEqual(criado.id, 4)

                atualizado = banco.atualizar(criado.id, quantidade="18")
                self.assertEqual(atualizado.quantidade, 18)

                banco_recarregado = ComponentRecord()
                self.assertEqual(banco_recarregado.buscar(criado.id).quantidade, 18)

                removido = banco_recarregado.remover(criado.id)
                self.assertEqual(removido.nome, "Sensor LDR")
                self.assertIsNone(banco_recarregado.buscar(criado.id))


if __name__ == "__main__":
    unittest.main()

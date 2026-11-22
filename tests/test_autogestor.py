import argparse
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import autogestor

APP = Path(autogestor.__file__).resolve()


class UnitTests(unittest.TestCase):
    def test_normaliza_placas(self):
        self.assertEqual(autogestor.plate(" abc-1234 "), "ABC1234")
        self.assertEqual(autogestor.plate("abc1d23"), "ABC1D23")

    def test_rejeita_placa_com_expansao_unicode(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            autogestor.plate("aß1234")

    def test_converte_valores_sem_arredondamento(self):
        self.assertEqual(autogestor.cents("100,05"), 10005)
        self.assertEqual(autogestor.money(10005), "R$ 100,05")
        for value in ("-1", "3.001", "NaN"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                autogestor.cents(value)


class IntegrationTests(unittest.TestCase):
    def test_chave_estrangeira_e_placa_unica(self):
        with sqlite3.connect(":memory:") as db:
            db.execute("PRAGMA foreign_keys = ON")
            db.executescript(autogestor.SCHEMA)
            query = "INSERT INTO veiculo(cliente_id, placa, modelo, ano) VALUES (?, ?, 'Modelo', 2020)"
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute(query, (99, "ABC1234"))
            db.execute("INSERT INTO cliente(nome, telefone, email) VALUES ('Exemplo', '', '')")
            db.execute(query, (1, "ABC1234"))
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute(query, (1, "ABC1234"))


class SystemTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.database = Path(temp.name) / "demo.sqlite3"

    def cli(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(APP), "--banco", str(self.database), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def setup_order(self):
        self.cli("cliente", "Cliente exemplo")
        self.cli("veiculo", "1", "abc-1234", "Modelo", "2020")
        self.cli("abrir-os", "ABC1234", "Revisão")

    def test_fluxo_completo_persiste_em_novos_processos(self):
        self.setup_order()
        self.cli("status-os", "1", "Em andamento")
        self.cli("servico", "1", "Inspeção", "90,10")
        self.cli("servico", "1", "Ajuste", "20,20")
        self.cli("status-os", "1", "Concluída")
        output = self.cli("consultar-os", "1")
        for fragment in ("Status: Concluída", "R$ 110,30", "Saída registrada", "Inspeção", "Ajuste"):
            self.assertIn(fragment, output)
        history = output.split("Histórico:", 1)[1]
        self.assertLess(history.index("Aberta"), history.index("Em andamento"))
        self.assertLess(history.index("Em andamento"), history.index("Concluída"))
        self.assertIn("não aceita", self.cli("servico", "1", "Outro", "10", code=1))

    def test_conclusao_invalida_nao_altera_historico(self):
        self.setup_order()
        self.assertIn("Transição inválida", self.cli("status-os", "1", "Concluída", code=1))
        self.cli("status-os", "1", "Em andamento")
        self.assertIn("pelo menos um serviço", self.cli("status-os", "1", "Concluída", code=1))
        output = self.cli("consultar-os", "1")
        self.assertIn("Status: Em andamento", output)
        self.assertNotIn("Concluída", output)

    def test_abre_banco_da_versao_0_1(self):
        legacy_schema = autogestor.SCHEMA.split("CREATE TABLE IF NOT EXISTS servico")[0]
        with sqlite3.connect(self.database) as db:
            db.executescript(legacy_schema)
            db.execute("INSERT INTO cliente(nome, telefone, email) VALUES ('Exemplo', '', '')")
            db.execute("INSERT INTO veiculo(cliente_id, placa, modelo, ano) VALUES (1, 'ABC1234', 'Modelo', 2020)")
            db.execute("INSERT INTO ordem(veiculo_id, entrada, observacoes) VALUES (1, '2026-11-16', 'Revisão')")
        self.assertIn("Status: Aberta", self.cli("consultar-os", "1"))
        self.cli("status-os", "1", "Em andamento")
        self.assertIn("Status: Em andamento", self.cli("consultar-os", "1"))

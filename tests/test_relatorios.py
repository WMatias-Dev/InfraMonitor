import csv
import json
import sys
from pathlib import Path
import tempfile
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from reports import gerar_relatorio_csv, gerar_relatorio_json, gerar_relatorios


def montar_registro(metrica, valor):
    return {
        "timestamp": "01/01/2026 00:00:00",
        "nivel": "INFO",
        "metrica": metrica,
        "valor": valor,
        "contexto": {"origem": "coleta_periodica"},
    }


class GeracaoRelatoriosTestCase(unittest.TestCase):
    def test_gera_relatorio_json_com_registros_originais(self):
        registros = [
            montar_registro("cpu", {"uso_percentual": 42}),
            montar_registro("memoria", {"uso_percentual": 61}),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "relatorio.json"
            retorno = gerar_relatorio_json(registros, caminho)

            self.assertEqual(retorno, caminho)

            with caminho.open("r", encoding="utf-8") as arquivo:
                conteudo = json.load(arquivo)

        self.assertEqual(conteudo["quantidade_registros"], 2)
        self.assertEqual(conteudo["registros"], registros)

    def test_gera_relatorio_csv_com_colunas_padrao(self):
        registros = [
            montar_registro("cpu", {"uso_percentual": 42}),
            montar_registro(
                "disco",
                {"particoes": [{"particao": "/dev/sda1", "ocupacao_percentual": 72}]},
            ),
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "relatorio.csv"
            retorno = gerar_relatorio_csv(registros, caminho)

            self.assertEqual(retorno, caminho)

            with caminho.open("r", encoding="utf-8") as arquivo:
                linhas = list(csv.DictReader(arquivo))

        self.assertEqual(len(linhas), 2)
        self.assertEqual(linhas[0]["metrica"], "cpu")
        self.assertIn("ocupacao_percentual", linhas[1]["valor"])

    def test_gera_relatorios_cria_json_e_csv(self):
        registros = [montar_registro("cpu", {"uso_percentual": 50})]

        with tempfile.TemporaryDirectory() as temp_dir:
            saida = gerar_relatorios(registros, temp_dir)

            self.assertTrue(saida["json"].exists())
            self.assertTrue(saida["csv"].exists())


if __name__ == "__main__":
    unittest.main()
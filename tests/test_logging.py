import json
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
import tempfile
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config import definir_configuracao
from logger import escrever_log, fechar_logger, obter_logger


class LoggingTestCase(unittest.TestCase):
    def setUp(self):
        definir_configuracao({})

    def test_obter_logger_usa_rotating_file_handler(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "inframonitor.log"
            logger = obter_logger(caminho)

            handlers = [handler for handler in logger.handlers if isinstance(handler, RotatingFileHandler)]

            fechar_logger(caminho)

        self.assertTrue(handlers)

    def test_escrever_log_grava_jsonl(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            caminho = Path(temp_dir) / "inframonitor.log"
            registro = {
                "timestamp": "01/01/2026 00:00:00",
                "nivel": "INFO",
                "metrica": "cpu",
                "valor": {"uso_percentual": 42},
                "contexto": {"origem": "teste"},
            }

            escrever_log(registro, caminho)
            fechar_logger(caminho)

            with caminho.open("r", encoding="utf-8") as arquivo:
                linha = arquivo.readline().strip()

        self.assertEqual(json.loads(linha), registro)


if __name__ == "__main__":
    unittest.main()
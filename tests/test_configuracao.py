import json
import sys
from pathlib import Path
import tempfile
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from alerts import obter_limites_alerta
from config import carregar_configuracao, definir_configuracao
from logger import obter_caminho_log
from reports import obter_diretorio_relatorios


class ConfiguracaoTestCase(unittest.TestCase):
    def test_carregar_configuracao_usa_arquivo_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            caminho_config = base_dir / "config.json"

            dados = {
                "intervalo_coleta_segundos": 12,
                "alertas": {
                    "cpu": {"warning": 70, "critical": 88},
                    "memoria": {"warning": 71, "critical": 89},
                    "disco": {"warning": 72, "critical": 90},
                },
                "logs": {
                    "diretorio": "custom-logs",
                    "nivel": "warning",
                    "max_bytes": 1024,
                    "backup_count": 2,
                },
                "relatorios": {
                    "diretorio": "custom-reports",
                },
            }

            with caminho_config.open("w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo)

            configuracao = carregar_configuracao(caminho_config)
            definir_configuracao(configuracao)

            self.assertEqual(configuracao["intervalo_coleta_segundos"], 12)
            self.assertEqual(configuracao["alertas"]["cpu"]["warning"], 70)
            self.assertEqual(configuracao["alertas"]["memoria"]["critical"], 89)
            self.assertEqual(configuracao["logs"]["nivel"], "WARNING")
            self.assertEqual(configuracao["logs"]["diretorio"], str((base_dir / "custom-logs").resolve()))
            self.assertEqual(
                configuracao["logs"]["arquivo"],
                str((base_dir / "custom-logs" / "infromonitor.log").resolve()),
            )
            self.assertEqual(configuracao["relatorios"]["diretorio"], str((base_dir / "custom-reports").resolve()))
            self.assertEqual(obter_caminho_log(), Path(configuracao["logs"]["arquivo"]))
            self.assertEqual(obter_diretorio_relatorios(), Path(configuracao["relatorios"]["diretorio"]))

            limites = obter_limites_alerta()
            self.assertEqual(limites["cpu"]["critical"], 88)
            self.assertEqual(limites["memoria"]["warning"], 71)
            self.assertEqual(limites["disco"]["warning"], 72)


if __name__ == "__main__":
    unittest.main()
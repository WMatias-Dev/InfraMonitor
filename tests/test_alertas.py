import sys
from pathlib import Path
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from alerts import avaliar_alertas


def montar_registro(metrica, valor):
    return {
        "timestamp": "01/01/2026 00:00:00",
        "nivel": "INFO",
        "metrica": metrica,
        "valor": valor,
        "contexto": {"origem": "teste"},
    }


class AvaliarAlertasTestCase(unittest.TestCase):
    def test_nao_gera_alerta_abaixo_dos_limites(self):
        registros = [
            montar_registro("cpu", {"uso_percentual": 40}),
            montar_registro("memoria", {"uso_percentual": 50}),
            montar_registro(
                "disco",
                {
                    "particoes": [
                        {"particao": "/dev/sda1", "uso_percentual": 60},
                        {"particao": "/dev/sda2", "uso_percentual": 62},
                    ]
                },
            ),
        ]

        limites = {
            "cpu": {"warning": 75, "critical": 90},
            "memoria": {"warning": 75, "critical": 90},
            "disco": {"warning": 80, "critical": 90},
        }

        self.assertEqual(avaliar_alertas(registros, limites), [])

    def test_gera_alerta_critico_de_disco_com_particao_maior(self):
        registros = [
            montar_registro("cpu", {"uso_percentual": 40}),
            montar_registro("memoria", {"uso_percentual": 50}),
            montar_registro(
                "disco",
                {
                    "particoes": [
                        {"particao": "/dev/sda1", "uso_percentual": 88},
                        {"particao": "/dev/sda2", "uso_percentual": 91},
                    ]
                },
            ),
        ]

        limites = {
            "cpu": {"warning": 75, "critical": 90},
            "memoria": {"warning": 75, "critical": 90},
            "disco": {"warning": 80, "critical": 90},
        }

        alertas = avaliar_alertas(registros, limites)

        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["metrica"], "alerta_disco")
        self.assertEqual(alertas[0]["nivel"], "CRITICAL")
        self.assertEqual(alertas[0]["valor"]["particao"], "/dev/sda2")
        self.assertEqual(alertas[0]["valor"]["uso_percentual"], 91)

    def test_gera_alerta_de_memoria_em_atencao(self):
        registros = [
            montar_registro("cpu", {"uso_percentual": 40}),
            montar_registro("memoria", {"uso_percentual": 78}),
            montar_registro("disco", {"particoes": [{"particao": "/dev/sda1", "uso_percentual": 40}]}),
        ]

        limites = {
            "cpu": {"warning": 75, "critical": 90},
            "memoria": {"warning": 75, "critical": 90},
            "disco": {"warning": 80, "critical": 90},
        }

        alertas = avaliar_alertas(registros, limites)

        self.assertEqual(len(alertas), 1)
        self.assertEqual(alertas[0]["metrica"], "alerta_memoria")
        self.assertEqual(alertas[0]["nivel"], "WARNING")
        self.assertEqual(alertas[0]["valor"]["limite_disparado"], 75)


if __name__ == "__main__":
    unittest.main()
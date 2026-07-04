import sys
from pathlib import Path

import pytest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from utils import formatar_bytes, formatar_data


def test_formatar_bytes_converte_em_unidades_adequadas():
    assert formatar_bytes(512) == "512.00 B"
    assert formatar_bytes(1024) == "1.00 KB"
    assert formatar_bytes(1024 * 1024) == "1.00 MB"


def test_formatar_data_formata_timestamp_em_padrão_br():
    from datetime import datetime

    assert formatar_data(0) == datetime.fromtimestamp(0).strftime("%d/%m/%Y %H:%M:%S")
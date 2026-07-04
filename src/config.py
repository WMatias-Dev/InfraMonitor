import json
import os
from pathlib import Path


CONFIGURACAO_APLICACAO = {}


def definir_configuracao(configuracao):
    global CONFIGURACAO_APLICACAO
    CONFIGURACAO_APLICACAO = configuracao or {}


def obter_configuracao():
    return CONFIGURACAO_APLICACAO


def _converter_para_inteiro(valor, padrao):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


def _converter_para_caminho(valor, padrao, base_dir=None):
    if not valor:
        return padrao

    caminho = Path(valor)
    if not caminho.is_absolute() and base_dir is not None:
        caminho = base_dir / caminho

    return str(caminho.resolve())


def _escolher_valor(*valores):
    for valor in valores:
        if valor not in (None, ""):
            return valor

    return None


def _configuracao_padrao():
    base_dir = Path(__file__).resolve().parent.parent
    return {
        "intervalo_coleta_segundos": 60,
        "alertas": {
            "cpu": {"warning": 75, "critical": 90},
            "memoria": {"warning": 75, "critical": 90},
            "disco": {"warning": 80, "critical": 90},
        },
        "logs": {
            "diretorio": str(base_dir / "logs"),
            "arquivo": str(base_dir / "logs" / "infromonitor.log"),
            "nivel": "INFO",
            "max_bytes": 5 * 1024 * 1024,
            "backup_count": 5,
        },
        "relatorios": {
            "diretorio": str(base_dir / "reports"),
        },
    }


def carregar_configuracao(caminho_config=None):
    caminho = Path(caminho_config) if caminho_config else Path(__file__).resolve().parent.parent / "config.json"
    base_dir = caminho.parent.resolve()
    configuracao = _configuracao_padrao()

    dados = {}
    if caminho.exists():
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    intervalo = _escolher_valor(dados.get("intervalo_coleta_segundos"), os.getenv("INTERVALO_COLETA_SEGUNDOS"))
    configuracao["intervalo_coleta_segundos"] = _converter_para_inteiro(
        intervalo,
        configuracao["intervalo_coleta_segundos"],
    )

    alertas = dados.get("alertas", {})
    alertas_env = {
        "cpu": {
            "warning": os.getenv("INFROMONITOR_CPU_WARNING_PERCENTUAL"),
            "critical": os.getenv("INFROMONITOR_CPU_CRITICAL_PERCENTUAL"),
        },
        "memoria": {
            "warning": os.getenv("INFROMONITOR_MEMORIA_WARNING_PERCENTUAL"),
            "critical": os.getenv("INFROMONITOR_MEMORIA_CRITICAL_PERCENTUAL"),
        },
        "disco": {
            "warning": os.getenv("INFROMONITOR_DISCO_WARNING_PERCENTUAL"),
            "critical": os.getenv("INFROMONITOR_DISCO_CRITICAL_PERCENTUAL"),
        },
    }

    for nome_metrica, limites_padrao in configuracao["alertas"].items():
        limites = alertas.get(nome_metrica, {})
        configuracao["alertas"][nome_metrica] = {
            "warning": _converter_para_inteiro(
                _escolher_valor(limites.get("warning"), alertas_env[nome_metrica]["warning"]),
                limites_padrao["warning"],
            ),
            "critical": _converter_para_inteiro(
                _escolher_valor(limites.get("critical"), alertas_env[nome_metrica]["critical"]),
                limites_padrao["critical"],
            ),
        }

    logs = dados.get("logs", {})
    if logs.get("diretorio"):
        configuracao["logs"]["diretorio"] = _converter_para_caminho(
            logs.get("diretorio"),
            configuracao["logs"]["diretorio"],
            base_dir,
        )

    arquivo_logs = _escolher_valor(logs.get("arquivo"), os.getenv("INFROMONITOR_LOG_FILE"))
    if arquivo_logs:
        configuracao["logs"]["arquivo"] = _converter_para_caminho(
            arquivo_logs,
            configuracao["logs"]["arquivo"],
            base_dir,
        )
    elif logs.get("diretorio"):
        configuracao["logs"]["arquivo"] = str(Path(configuracao["logs"]["diretorio"]) / "infromonitor.log")

    configuracao["logs"]["nivel"] = str(
        _escolher_valor(logs.get("nivel"), os.getenv("INFROMONITOR_LOG_LEVEL"), configuracao["logs"]["nivel"])
    ).upper()
    configuracao["logs"]["max_bytes"] = _converter_para_inteiro(
        _escolher_valor(logs.get("max_bytes"), os.getenv("INFROMONITOR_LOG_MAX_BYTES")),
        configuracao["logs"]["max_bytes"],
    )
    configuracao["logs"]["backup_count"] = _converter_para_inteiro(
        _escolher_valor(logs.get("backup_count"), os.getenv("INFROMONITOR_LOG_BACKUP_COUNT")),
        configuracao["logs"]["backup_count"],
    )

    relatorios = dados.get("relatorios", {})
    configuracao["relatorios"]["diretorio"] = _converter_para_caminho(
        _escolher_valor(relatorios.get("diretorio"), os.getenv("INFROMONITOR_REPORT_DIR")),
        configuracao["relatorios"]["diretorio"],
        base_dir,
    )

    return configuracao
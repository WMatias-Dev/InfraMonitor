import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import obter_configuracao


_LOGGERS = {}


def _converter_para_inteiro(valor, padrao):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return padrao


def obter_caminho_log():
    configuracao = obter_configuracao()
    logs_configurados = configuracao.get("logs", {})
    caminho_configurado = logs_configurados.get("arquivo")

    if not caminho_configurado and logs_configurados.get("diretorio"):
        caminho_configurado = str(Path(logs_configurados["diretorio"]) / "infromonitor.log")

    if caminho_configurado:
        return Path(caminho_configurado)

    return Path(__file__).resolve().parent.parent / "logs" / "infromonitor.log"


def obter_logger(caminho_log=None):
    caminho = Path(caminho_log) if caminho_log else obter_caminho_log()
    chave_cache = str(caminho.resolve())

    if chave_cache in _LOGGERS:
        return _LOGGERS[chave_cache]

    caminho.parent.mkdir(parents=True, exist_ok=True)

    logs_configurados = obter_configuracao().get("logs", {})
    nivel_log = str(logs_configurados.get("nivel") or "INFO").upper()
    max_bytes = _converter_para_inteiro(logs_configurados.get("max_bytes"), 5 * 1024 * 1024)
    backup_count = _converter_para_inteiro(logs_configurados.get("backup_count"), 5)

    logger = logging.getLogger(f"inframonitor.{chave_cache}")
    logger.setLevel(getattr(logging, nivel_log, logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        handler = RotatingFileHandler(
            caminho,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

    _LOGGERS[chave_cache] = logger
    return logger


def escrever_log(registro, caminho_log=None):
    logger = obter_logger(caminho_log)
    logger.info(json.dumps(registro, ensure_ascii=False))


def fechar_logger(caminho_log=None):
    caminho = Path(caminho_log) if caminho_log else obter_caminho_log()
    chave_cache = str(caminho.resolve())
    logger = _LOGGERS.pop(chave_cache, None)

    if logger is None:
        return

    for handler in list(logger.handlers):
        handler.flush()
        handler.close()
        logger.removeHandler(handler)
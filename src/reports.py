import csv
import json
import time
from pathlib import Path

from config import obter_configuracao
from utils import formatar_data


def _gerar_nome_relatorio(sufixo, extensao):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"relatorio_{sufixo}_{timestamp}.{extensao}"


def _serializar_valor_csv(valor):
    return json.dumps(valor, ensure_ascii=False)


def obter_diretorio_relatorios():
    configuracao = obter_configuracao()
    diretorio_configurado = configuracao.get("relatorios", {}).get("diretorio")

    if diretorio_configurado:
        return Path(diretorio_configurado)

    return Path(__file__).resolve().parent.parent / "reports"


def gerar_relatorio_json(registros, caminho_relatorio=None):
    if caminho_relatorio is None:
        diretorio = obter_diretorio_relatorios()
        caminho_relatorio = diretorio / _gerar_nome_relatorio("metricas", "json")
    else:
        caminho_relatorio = Path(caminho_relatorio)

    caminho_relatorio.parent.mkdir(parents=True, exist_ok=True)

    conteudo = {
        "gerado_em": formatar_data(time.time()),
        "quantidade_registros": len(registros),
        "registros": registros,
    }

    with caminho_relatorio.open("w", encoding="utf-8") as arquivo:
        json.dump(conteudo, arquivo, ensure_ascii=False, indent=2)

    return caminho_relatorio


def gerar_relatorio_csv(registros, caminho_relatorio=None):
    if caminho_relatorio is None:
        diretorio = obter_diretorio_relatorios()
        caminho_relatorio = diretorio / _gerar_nome_relatorio("metricas", "csv")
    else:
        caminho_relatorio = Path(caminho_relatorio)

    caminho_relatorio.parent.mkdir(parents=True, exist_ok=True)

    campos = ["timestamp", "nivel", "metrica", "contexto", "valor"]

    with caminho_relatorio.open("w", newline="", encoding="utf-8") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=campos)
        writer.writeheader()

        for registro in registros:
            writer.writerow(
                {
                    "timestamp": registro.get("timestamp"),
                    "nivel": registro.get("nivel"),
                    "metrica": registro.get("metrica"),
                    "contexto": _serializar_valor_csv(registro.get("contexto", {})),
                    "valor": _serializar_valor_csv(registro.get("valor", {})),
                }
            )

    return caminho_relatorio


def gerar_relatorios(registros, diretorio_relatorios=None):
    diretorio = Path(diretorio_relatorios) if diretorio_relatorios else obter_diretorio_relatorios()
    return {
        "json": gerar_relatorio_json(registros, diretorio / _gerar_nome_relatorio("metricas", "json")),
        "csv": gerar_relatorio_csv(registros, diretorio / _gerar_nome_relatorio("metricas", "csv")),
    }
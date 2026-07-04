from datetime import datetime


def formatar_bytes(valor):
    """Converte bytes para KB, MB, GB..."""
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if valor < 1024:
            return f"{valor:.2f} {unidade}"
        valor /= 1024


def formatar_data(valor_timestamp):
    return datetime.fromtimestamp(valor_timestamp).strftime("%d/%m/%Y %H:%M:%S")

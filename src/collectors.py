import platform
import time
from datetime import datetime

import psutil

from utils import formatar_bytes, formatar_data


def montar_registro(nivel, metrica, valor, contexto=None):
    return {
        "timestamp": formatar_data(time.time()),
        "nivel": nivel,
        "metrica": metrica,
        "valor": valor,
        "contexto": contexto or {},
    }


def coletar_cpu():
    try:
        return montar_registro(
            "INFO",
            "cpu",
            {
                "nucleos_logicos": psutil.cpu_count(),
                "nucleos_fisicos": psutil.cpu_count(logical=False),
                "uso_percentual": psutil.cpu_percent(interval=1),
            },
            {"origem": "coleta_periodica"},
        )
    except Exception as erro:
        return montar_registro("ERROR", "cpu", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def coletar_memoria():
    try:
        mem = psutil.virtual_memory()
        return montar_registro(
            "INFO",
            "memoria",
            {
                "total": formatar_bytes(mem.total),
                "em_uso": formatar_bytes(mem.used),
                "disponivel": formatar_bytes(mem.available),
                "uso_percentual": mem.percent,
            },
            {"origem": "coleta_periodica"},
        )
    except Exception as erro:
        return montar_registro("ERROR", "memoria", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def coletar_bateria():
    try:
        bat = psutil.sensors_battery()

        if bat is None:
            return montar_registro(
                "INFO",
                "bateria",
                {"disponivel": False, "mensagem": "Este dispositivo não possui bateria."},
                {"origem": "coleta_periodica"},
            )

        return montar_registro(
            "INFO",
            "bateria",
            {
                "disponivel": True,
                "nivel_percentual": bat.percent,
                "na_tomada": bat.power_plugged,
            },
            {"origem": "coleta_periodica"},
        )

    except Exception as erro:
        return montar_registro("ERROR", "bateria", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def coletar_sistema():
    try:
        inicio = datetime.fromtimestamp(psutil.boot_time())
        return montar_registro(
            "INFO",
            "sistema",
            {
                "sistema_operacional": f"{platform.system()} {platform.release()}",
                "iniciado_em": inicio.strftime("%d/%m/%Y %H:%M:%S"),
            },
            {"origem": "coleta_periodica"},
        )

    except Exception as erro:
        return montar_registro("ERROR", "sistema", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def coletar_disco():
    try:
        particoes = []

        for part in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(part.mountpoint)

                particoes.append(
                    {
                        "particao": part.device,
                        "total": formatar_bytes(uso.total),
                        "usado": formatar_bytes(uso.used),
                        "livre": formatar_bytes(uso.free),
                        "uso_percentual": uso.percent,
                    }
                )

            except PermissionError:
                continue

        return montar_registro(
            "INFO",
            "disco",
            {"particoes": particoes},
            {"origem": "coleta_periodica"},
        )

    except Exception as erro:
        return montar_registro("ERROR", "disco", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def coletar_rede():
    try:
        net = psutil.net_io_counters()
        return montar_registro(
            "INFO",
            "rede",
            {
                "enviado": formatar_bytes(net.bytes_sent),
                "recebido": formatar_bytes(net.bytes_recv),
            },
            {"origem": "coleta_periodica"},
        )
    except Exception as erro:
        return montar_registro("ERROR", "rede", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def coletar_processos():
    try:
        processos = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                processos.append({"pid": proc.info["pid"], "nome": proc.info["name"]})
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return montar_registro(
            "INFO",
            "processos",
            {"processos": processos},
            {"origem": "coleta_periodica"},
        )

    except Exception as erro:
        return montar_registro("ERROR", "processos", {"erro": str(erro)}, {"origem": "coleta_periodica"})


def detalhar_processo(pid):
    try:
        proc = psutil.Process(pid)

        tempo = time.time() - proc.create_time()
        return montar_registro(
            "INFO",
            "processo",
            {
                "pid": pid,
                "nome": proc.name(),
                "status": proc.status(),
                "cpu_percentual": proc.cpu_percent(interval=1),
                "memoria": formatar_bytes(proc.memory_info().rss),
                "tempo_ativo_segundos": f"{tempo:.2f}",
            },
            {"origem": "detalhe_manual"},
        )

    except psutil.NoSuchProcess:
        return montar_registro("ERROR", "processo", {"pid": pid, "erro": "Processo não encontrado."}, {"origem": "detalhe_manual"})
    except psutil.AccessDenied:
        return montar_registro(
            "ERROR",
            "processo",
            {"pid": pid, "erro": "Sem permissão para acessar este processo."},
            {"origem": "detalhe_manual"},
        )
    except Exception as erro:
        return montar_registro("ERROR", "processo", {"pid": pid, "erro": str(erro)}, {"origem": "detalhe_manual"})


def coletar_metricas():
    return [coletar_cpu(), coletar_memoria(), coletar_disco()]


mostrar_cpu = coletar_cpu
mostrar_memoria = coletar_memoria
mostrar_bateria = coletar_bateria
mostrar_sistema = coletar_sistema
mostrar_disco = coletar_disco
mostrar_rede = coletar_rede
listar_processos = coletar_processos
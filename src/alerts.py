from config import obter_configuracao


def _obter_percentual_maximo_disco(registro_disco):
    if not registro_disco:
        return None, None

    particoes = registro_disco["valor"].get("particoes", [])
    if not particoes:
        return None, None

    particao_maior = max(
        particoes,
        key=lambda particao: particao.get("uso_percentual") if particao.get("uso_percentual") is not None else -1,
    )
    percentual = particao_maior.get("uso_percentual")

    if percentual is None:
        return None, None

    return percentual, particao_maior.get("particao")


def obter_limites_alerta():
    configuracao = obter_configuracao()
    alertas_configurados = configuracao.get("alertas", {})

    return {
        "cpu": {
            "warning": alertas_configurados.get("cpu", {}).get("warning", 75),
            "critical": alertas_configurados.get("cpu", {}).get("critical", 90),
        },
        "memoria": {
            "warning": alertas_configurados.get("memoria", {}).get("warning", 75),
            "critical": alertas_configurados.get("memoria", {}).get("critical", 90),
        },
        "disco": {
            "warning": alertas_configurados.get("disco", {}).get("warning", 80),
            "critical": alertas_configurados.get("disco", {}).get("critical", 90),
        },
    }


def avaliar_alertas(registros, limites=None):
    from collectors import montar_registro

    limites = limites or obter_limites_alerta()

    cpu = next((registro for registro in registros if registro["metrica"] == "cpu"), None)
    memoria = next((registro for registro in registros if registro["metrica"] == "memoria"), None)
    disco = next((registro for registro in registros if registro["metrica"] == "disco"), None)

    disco_percentual, disco_particao = _obter_percentual_maximo_disco(disco)

    metricas = [
        ("cpu", cpu["valor"].get("uso_percentual") if cpu else None, limites.get("cpu", {}), None),
        ("memoria", memoria["valor"].get("uso_percentual") if memoria else None, limites.get("memoria", {}), None),
        ("disco", disco_percentual, limites.get("disco", {}), disco_particao),
    ]

    alertas = []

    for nome_metrica, percentual, limite_config, particao in metricas:
        if percentual is None:
            continue

        limite_warning = limite_config.get("warning")
        limite_critico = limite_config.get("critical")

        if limite_critico is not None and percentual >= limite_critico:
            nivel = "CRITICAL"
            status = "CRITICO"
            limite_disparado = limite_critico
            mensagem = f"Uso crítico de {nome_metrica} identificado."
        elif limite_warning is not None and percentual >= limite_warning:
            nivel = "WARNING"
            status = "ATENCAO"
            limite_disparado = limite_warning
            mensagem = f"Uso elevado de {nome_metrica} identificado."
        else:
            continue

        valor = {
            "status": status,
            "mensagem": mensagem,
            "uso_percentual": percentual,
            "limite_disparado": limite_disparado,
            "limites": {
                "warning": limite_warning,
                "critical": limite_critico,
            },
        }

        if particao is not None:
            valor["particao"] = particao

        alertas.append(
            montar_registro(
                nivel,
                f"alerta_{nome_metrica}",
                valor,
                {"origem": "alerta_automatico"},
            )
        )

    return alertas


def resumir_metricas(registros):
    from collectors import montar_registro

    cpu = next((registro for registro in registros if registro["metrica"] == "cpu"), None)
    memoria = next((registro for registro in registros if registro["metrica"] == "memoria"), None)
    disco = next((registro for registro in registros if registro["metrica"] == "disco"), None)

    cpu_percentual = cpu["valor"].get("uso_percentual") if cpu else None
    memoria_percentual = memoria["valor"].get("uso_percentual") if memoria else None

    disco_percentual = None
    if disco:
        disco_percentual, _ = _obter_percentual_maximo_disco(disco)

    maior_percentual = max(
        [valor for valor in [cpu_percentual, memoria_percentual, disco_percentual] if valor is not None],
        default=None,
    )

    if maior_percentual is None:
        nivel = "INFO"
        status = "SEM_DADOS"
        mensagem = "Resumo indisponível por ausência de métricas válidas."
    elif maior_percentual >= 90:
        nivel = "CRITICAL"
        status = "CRITICO"
        mensagem = "Sistema com uso crítico de recursos."
    elif maior_percentual >= 75:
        nivel = "WARNING"
        status = "ATENCAO"
        mensagem = "Sistema com uso elevado de recursos."
    else:
        nivel = "INFO"
        status = "OK"
        mensagem = "Sistema em condição estável."

    return montar_registro(
        nivel,
        "resumo_saude",
        {
            "status": status,
            "mensagem": mensagem,
            "cpu_percentual": cpu_percentual,
            "memoria_percentual": memoria_percentual,
            "disco_percentual_maximo": disco_percentual,
        },
        {"origem": "resumo_automatico"},
    )
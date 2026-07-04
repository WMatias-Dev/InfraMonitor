from config import obter_configuracao


def _obter_ocupacao_maxima_disco(registro_disco):
    if not registro_disco:
        return None, None

    particoes = registro_disco["valor"].get("particoes", [])
    if not particoes:
        return None, None

    particao_maior = max(
        particoes,
        key=lambda particao: particao.get("ocupacao_percentual")
        if particao.get("ocupacao_percentual") is not None
        else -1,
    )
    percentual = particao_maior.get("ocupacao_percentual")

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

    def _mensagem_alerta(nome_metrica, nivel):
        if nome_metrica == "cpu":
            return "Uso de CPU crítico identificado." if nivel == "CRITICAL" else "Uso de CPU elevado identificado."

        if nome_metrica == "memoria":
            return (
                "Uso de memória RAM crítico identificado."
                if nivel == "CRITICAL"
                else "Uso de memória RAM elevado identificado."
            )

        return (
            "Ocupação de espaço em disco crítica identificada."
            if nivel == "CRITICAL"
            else "Ocupação de espaço em disco elevada identificada."
        )

    limites = limites or obter_limites_alerta()

    cpu = next((registro for registro in registros if registro["metrica"] == "cpu"), None)
    memoria = next((registro for registro in registros if registro["metrica"] == "memoria"), None)
    disco = next((registro for registro in registros if registro["metrica"] == "disco"), None)

    disco_percentual, disco_particao = _obter_ocupacao_maxima_disco(disco)

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
            mensagem = _mensagem_alerta(nome_metrica, nivel)
        elif limite_warning is not None and percentual >= limite_warning:
            nivel = "WARNING"
            status = "ATENCAO"
            limite_disparado = limite_warning
            mensagem = _mensagem_alerta(nome_metrica, nivel)
        else:
            continue

        valor = {
            "status": status,
            "mensagem": mensagem,
            "ocupacao_percentual" if nome_metrica == "disco" else "uso_percentual": percentual,
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

    def _mensagem_resumo(nome_metrica, nivel):
        if nome_metrica == "cpu":
            return "Uso de CPU crítico." if nivel == "CRITICAL" else "Uso de CPU elevado."

        if nome_metrica == "memoria":
            return "Uso de memória RAM crítico." if nivel == "CRITICAL" else "Uso de memória RAM elevado."

        return (
            "Ocupação de espaço em disco crítica."
            if nivel == "CRITICAL"
            else "Ocupação de espaço em disco elevada."
        )

    cpu = next((registro for registro in registros if registro["metrica"] == "cpu"), None)
    memoria = next((registro for registro in registros if registro["metrica"] == "memoria"), None)
    disco = next((registro for registro in registros if registro["metrica"] == "disco"), None)

    cpu_percentual = cpu["valor"].get("uso_percentual") if cpu else None
    memoria_percentual = memoria["valor"].get("uso_percentual") if memoria else None

    disco_percentual = None
    if disco:
        disco_percentual, _ = _obter_ocupacao_maxima_disco(disco)

    metricas_validas = [
        ("cpu", cpu_percentual),
        ("memoria", memoria_percentual),
        ("disco", disco_percentual),
    ]
    metricas_validas = [item for item in metricas_validas if item[1] is not None]
    maior_nome, maior_percentual = max(metricas_validas, key=lambda item: item[1], default=(None, None))

    if maior_percentual is None:
        nivel = "INFO"
        status = "SEM_DADOS"
        mensagem = "Resumo indisponível por ausência de métricas válidas."
    elif maior_percentual >= 90:
        nivel = "CRITICAL"
        status = "CRITICO"
        mensagem = _mensagem_resumo(maior_nome, nivel)
    elif maior_percentual >= 75:
        nivel = "WARNING"
        status = "ATENCAO"
        mensagem = _mensagem_resumo(maior_nome, nivel)
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
            "ocupacao_percentual_maxima_disco": disco_percentual,
        },
        {"origem": "resumo_automatico"},
    )
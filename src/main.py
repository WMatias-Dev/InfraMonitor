import os

from monitor import executar_coleta_periodica


def carregar_configuracao():
    intervalo = os.getenv("INTERVALO_COLETA_SEGUNDOS", "60")

    try:
        intervalo = int(intervalo)
    except ValueError:
        intervalo = 60

    return {
        "intervalo_coleta_segundos": intervalo,
    }


if __name__ == "__main__":
    configuracao = carregar_configuracao()
    executar_coleta_periodica(configuracao["intervalo_coleta_segundos"])

import time

from alerts import avaliar_alertas, resumir_metricas
from collectors import coletar_metricas
from logger import escrever_log, obter_caminho_log


def executar_coleta_periodica(intervalo_segundos=60, caminho_log=None):
    caminho_log = caminho_log or obter_caminho_log()

    while True:
        registros = coletar_metricas()
        alertas = avaliar_alertas(registros)
        resumo = resumir_metricas(registros)

        for registro in registros:
            escrever_log(registro, caminho_log)

        for alerta in alertas:
            escrever_log(alerta, caminho_log)

        escrever_log(resumo, caminho_log)
        time.sleep(intervalo_segundos)
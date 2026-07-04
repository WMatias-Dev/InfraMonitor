from config import carregar_configuracao, definir_configuracao
from monitor import executar_coleta_periodica


if __name__ == "__main__":
    configuracao = carregar_configuracao()
    definir_configuracao(configuracao)
    executar_coleta_periodica(configuracao["intervalo_coleta_segundos"])

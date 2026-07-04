import psutil
import platform
import time
from datetime import datetime


# =========================
# UTILIDADES
# =========================
def formatar_bytes(valor):
    """Converte bytes para KB, MB, GB..."""
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if valor < 1024:
            return f"{valor:.2f} {unidade}"
        valor /= 1024


# =========================
# INFORMAÇÕES DO SISTEMA
# =========================
def mostrar_cpu():
    print("\n--- CPU ---")
    try:
        print(f"Núcleos lógicos : {psutil.cpu_count()}")
        print(f"Núcleos físicos : {psutil.cpu_count(logical=False)}")
        print(f"Uso atual       : {psutil.cpu_percent(interval=1)}%")
    except Exception as erro:
        print(f"Não foi possível obter dados da CPU: {erro}")


def mostrar_memoria():
    print("\n--- MEMÓRIA ---")
    try:
        mem = psutil.virtual_memory()
        print(f"Total       : {formatar_bytes(mem.total)}")
        print(f"Em uso      : {formatar_bytes(mem.used)}")
        print(f"Disponível  : {formatar_bytes(mem.available)}")
        print(f"Uso (%)     : {mem.percent}%")
    except Exception as erro:
        print(f"Erro ao obter memória: {erro}")


def mostrar_bateria():
    print("\n--- BATERIA ---")
    try:
        bat = psutil.sensors_battery()

        if bat is None:
            print("Este dispositivo não possui bateria.")
            return

        print(f"Nível: {bat.percent}%")
        print("Na tomada:", "Sim" if bat.power_plugged else "Não")

    except Exception as erro:
        print(f"Erro ao obter bateria: {erro}")


def mostrar_sistema():
    print("\n--- SISTEMA ---")
    try:
        print(f"Sistema operacional: {platform.system()} {platform.release()}")

        inicio = datetime.fromtimestamp(psutil.boot_time())
        print(f"Iniciado em: {inicio.strftime('%d/%m/%Y %H:%M:%S')}")

    except Exception as erro:
        print(f"Erro ao obter sistema: {erro}")


def mostrar_disco():
    print("\n--- DISCO ---")
    try:
        for part in psutil.disk_partitions():
            try:
                uso = psutil.disk_usage(part.mountpoint)

                print(f"\nPartição: {part.device}")
                print(f"Total   : {formatar_bytes(uso.total)}")
                print(f"Usado   : {formatar_bytes(uso.used)}")
                print(f"Livre   : {formatar_bytes(uso.free)}")
                print(f"Uso (%) : {uso.percent}%")

            except PermissionError:
                continue

    except Exception as erro:
        print(f"Erro ao obter disco: {erro}")


def mostrar_rede():
    print("\n--- REDE ---")
    try:
        net = psutil.net_io_counters()
        print(f"Enviado : {formatar_bytes(net.bytes_sent)}")
        print(f"Recebido: {formatar_bytes(net.bytes_recv)}")
    except Exception as erro:
        print(f"Erro ao obter rede: {erro}")


# =========================
# PROCESSOS
# =========================
def listar_processos():
    print("\n--- PROCESSOS EM EXECUÇÃO ---")
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            try:
                print(f"{proc.info['pid']:>6} | {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    except Exception as erro:
        print(f"Erro ao listar processos: {erro}")


def detalhar_processo(pid):
    print(f"\n--- DETALHES DO PROCESSO ({pid}) ---")
    try:
        proc = psutil.Process(pid)

        print(f"Nome       : {proc.name()}")
        print(f"Status     : {proc.status()}")
        print(f"CPU (%)    : {proc.cpu_percent(interval=1)}")
        print(f"Memória    : {formatar_bytes(proc.memory_info().rss)}")

        tempo = time.time() - proc.create_time()
        print(f"Tempo ativo: {tempo:.2f} segundos")

    except psutil.NoSuchProcess:
        print("Processo não encontrado.")
    except psutil.AccessDenied:
        print("Sem permissão para acessar este processo.")
    except Exception as erro:
        print(f"Erro inesperado: {erro}")


# =========================
# MENU
# =========================
def menu():
    opcoes = {
        "1": mostrar_cpu,
        "2": mostrar_memoria,
        "3": listar_processos,
        "5": mostrar_bateria,
        "6": mostrar_sistema,
        "7": mostrar_disco,
        "8": mostrar_rede
    }

    while True:
        print("\n==============================")
        print("   MONITOR DE SISTEMA")
        print("==============================")
        print("1 - CPU")
        print("2 - Memória")
        print("3 - Listar processos")
        print("4 - Detalhar processo (PID)")
        print("5 - Bateria")
        print("6 - Sistema")
        print("7 - Disco")
        print("8 - Rede")
        print("0 - Sair")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "0":
            print("Encerrando...")
            break

        elif escolha == "4":
            try:
                pid = int(input("Digite o PID: "))
                detalhar_processo(pid)
            except ValueError:
                print("PID inválido.")

        elif escolha in opcoes:
            opcoes[escolha]()

        else:
            print("Opção inválida. Tente novamente.")


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    menu()
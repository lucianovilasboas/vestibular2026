import os
import time
from datetime import datetime
import shutil

download_dir = "/mnt/Data/Dev/python_projects/vestibular2026/dados/input"

# Nome do arquivo esperado
nome_originais = [("export.csv","INT"), ("export (1).csv","SUB"), ("export (2).csv","SUP")]

# Nome novo com data
data_atual = datetime.now().strftime("%Y%m%d_%H%M")

for nome_original, tipo in nome_originais:
    novo_nome = f"dados_{tipo}_{data_atual}.csv"

    # Caminho completo
    arquivo_origem = os.path.join(download_dir, nome_original)
    arquivo_destino = os.path.join(download_dir, novo_nome)

    # Aguarda o download terminar (export.csv aparecer)
    timeout = 60  # até 1 minuto
    for _ in range(timeout):
        if os.path.exists(arquivo_origem):
            # Dá uma folga para garantir que terminou de escrever
            time.sleep(2)
            shutil.move(arquivo_origem, arquivo_destino)
            print(f"Arquivo renomeado para: {arquivo_destino}")
            break
        time.sleep(1)
    else:
        print("Arquivo export.csv não foi encontrado para renomear.")

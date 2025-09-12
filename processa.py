import pandas as pd
import os
from datetime import datetime
import shutil 
from log import logger

if __name__ == "__main__":
    
    # Define os caminhos das pastas
    dados_folder = "./dados"
    input_folder = "./dados/input"
    processed_folder = "./dados/processed"
    backup_folder = "./dados/backup"
    timestamp = datetime.now()
    # Gera o novo nome para o arquivo com base na data de leitura
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")

    # Tenta listar todos os arquivos na pasta de entrada
    try:
        files = os.listdir(input_folder)
        if not files:
            print(f"{timestamp_str} - Nenhum arquivo encontrado na pasta input.")
            logger.warn(f"Nenhum arquivo encontrado na pasta input.")
            exit()
    except Exception as e:
        print(f"{timestamp_str} - Nenhum arquivo encontrado na pasta input.")
        logger.warn(f"Nenhum arquivo encontrado na pasta input - {e}")
        exit()

    # lendo o dataframe final
    df_all = pd.read_csv("./dados/processed/all_data.csv")
    dataframes = []
    if not df_all.empty:
        dataframes.append(df_all)

    for file in files:
        if file.endswith('.csv'):
            # Define o caminho completo do arquivo
            file_path = os.path.join(input_folder, file)

            # Lê o arquivo CSV
            df = pd.read_csv(file_path)
            
            # Ajusta os totais
            df = ajustar_totais(df)

            # Registra o timestamp da leitura
            df['Timestamp'] = timestamp
            df["Modalidade"] = file.split("_")[1]

            dataframes.append(df)

            shutil.move(file_path, os.path.join(backup_folder, file))


    csv_file_path = os.path.join(processed_folder, "all_data")
    df_all = pd.concat(dataframes)
    df_all.to_csv(f"{csv_file_path}.csv", index=False, encoding="utf-8")

    print(f"{timestamp_str} - Todos os arquivos processados e movidos com sucesso!")
    logger.info(f"Todos os arquivos processados e movidos com sucesso!")
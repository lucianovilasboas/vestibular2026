import schedule
import subprocess
import time
from log import logger

# Função para executar os scripts 
def executar():
    print("  Executando automacao.py...")
    logger.info("  Executando automacao.py...")
    subprocess.run(["python", "automacao.py"])
    logger.info("  Execução finalizada.")

    print("  Executando renomeia.py...")
    logger.info("  Executando renomeia.py...")
    subprocess.run(["python", "renomeia.py"])
    logger.info("  Execução finalizada.")

    print("  Executando processa.py...")
    logger.info("  Executando processa.py...")
    subprocess.run(["python", "processa.py"])
    logger.info("  Execução finalizada.")

    print("  Executando gitrun.py...")
    logger.info("  Executando gitrun.py...")
    subprocess.run(["python", "gitrun.py", "-m", "data update using git"])
    logger.info("  Execução finalizada.")



if __name__ == "__main__":
    logger.info(f"Execução via 'run.py' inicializada às {time.strftime('%d-%m-%Y %H:%M:%S')}")
    executar()
    logger.info(f"Execução via 'run.py' finalizada às {time.strftime('%d-%m-%Y %H:%M:%S')}")

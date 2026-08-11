import logging
import os
from datetime import datetime

from ingestion.core.config import OUTPUT_DIR


def get_logger(name: str):

    os.makedirs(
        f"{OUTPUT_DIR}/logs",
        exist_ok=True
    )

    log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"

    log_path = os.path.join(
        OUTPUT_DIR,
        "logs",
        log_filename
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Arquivo
    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Guarda o caminho do arquivo de log
    logger.log_path = log_path

    return logger